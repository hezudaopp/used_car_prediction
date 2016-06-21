# -*- coding: UTF-8 -*-

from sklearn import linear_model

import utils
import db
import config
import numpy as np
import regression as rgr

class CarPricePredict:
	"""predict car price.
	train data_set size and scope will also be returned."""
	def predict(self):
		train_X, train_Y, predict_X, i = self._prepare_data(self.brand_id, self.series_id, self.model_id, self.province_id)
		if len(train_X) < config.MIN_TRAIN_NUM:
			return -1, -1, i
		predict_Y = self._ols(train_X, train_Y, predict_X)
		return int(predict_Y), len(train_X), i

	"""ordinary least squar"""
	def _ols(self, dataX, dataY, predict_X):
		regr = linear_model.LinearRegression()
		regr.fit(dataX, dataY)
		return regr.predict(predict_X)[0]

	"""locally weighted linear regression implemented"""
	def _lwlr(self, train_X, train_Y, predictX):
		if len(train_X) < config.NUM_FEATURE[config.FEATURE_NAME]:
			return -1
		return rgr.lwlr(predictX, train_X, train_Y, k=100000000)

	"""predict used car price"""
	def __init__(self, brand_id, series_id, model_id, province_id, card_month, mileage):
		self.brand_id = brand_id
		self.series_id =  series_id
		self.model_id = model_id
		self.province_id = province_id
		self.card_time = utils.convert_month_to_timestamp(card_month)
		if self.card_time == -1:
			return None
		self.mileage = mileage * 10000

	"""prepare training data_set"""
	def _prepare_data(self, brand_id, series_id, model_id=None, province_id=None):
		i = 1
		deal_province_offset = 0
		# try to filter training data by series_id, model_id and province_id,
		# if training set is not enough, remove province_id constraint
		while i >= 0:
			if (i & (1 << deal_province_offset)) > 0:
				tmp_province_id = province_id
			else:
				tmp_province_id = None
			data_set = db.allnet_price(brand_id, series_id, model_id, tmp_province_id)
			if len(data_set) >= config.MIN_TRAIN_NUM:
				break
			i = i - 1
		# if training set is not enough, return empty training data_set.
		if len(data_set) < config.MIN_TRAIN_NUM: return [], [], [], i

		# filter data
		dataX, dataY = self._filter_data(data_set)
		# if train data_set's size is smaller than feature number, return empty training data_set
		if len(dataX) < config.NUM_FEATURE[config.FEATURE_NAME]: return [], [], [], i

		predictX = [[self.card_time, utils.NOW, self.mileage]]
		if config.FEATURE_NAME == config.FEATURE_NAME_USAGE_TIME:
			predictX = [[utils.NOW - self.card_time, self.mileage]]
		return dataX, dataY, predictX, i

	"""filter training data_set, exclude noise"""
	def _filter_data(self, data_set):
		filtered_data = []
		for i in range(len(data_set)):
			# if price much less or more than deal price
			# if data_set[i][-1] > (data_set[i][-2] * 1.5) or data_set[i][-1] < (data_set[i][-2] * 0.5): continue
			# if card time later than deal time
			if data_set[i][0] >= data_set[i][1]: continue
			# if mileage is less than 100km or more than 1000000km
			if data_set[i][2] <= 100 or data_set[i][2] >= 1000000: continue
			filtered_data.append(data_set[i])
		if len(filtered_data) < 1: return filtered_data

		filtered_data = np.array(filtered_data)
		if config.FEATURE_NAME == config.FEATURE_NAME_USAGE_TIME:
			filtered_data[:, 0] = filtered_data[:, 1] - filtered_data[:, 0]
			filtered_data[:, 1] = filtered_data[:, 2]

		# filter point which is far away from predicted mean line
		if config.FILTER_FEATURE_BY_DISTINCE:
			regr = linear_model.LinearRegression()
			# first NUM_FEATURE columns are feature columns
			dataX = filtered_data[:, :config.NUM_FEATURE[config.FEATURE_NAME]]
			# last column is value column
			dataY = filtered_data[:, -1]
			if len(dataX) < config.MIN_TRAIN_NUM:
				return filtered_data
			regr.fit(dataX, dataY)
			distances = dataY - regr.predict(dataX)
			# filter by distance confidence interval
			# print len(filtered_data),
			mean, low_confidenc_limit, high_confidence_limit = utils.mean_confidence_interval(distances, confidence=0.99)
			filtered_data = np.array([filtered_data[i] for i in range(len(filtered_data)) if distances[i] >= low_confidenc_limit and distances[i] <= high_confidence_limit])
			# print len(filtered_data)

		return filtered_data[:, :config.NUM_FEATURE[config.FEATURE_NAME]], filtered_data[:, -1]

