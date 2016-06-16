# -*- coding: UTF-8 -*-

from sklearn import linear_model

import utils
import db
import numpy as np
import regression as rgr

class CarPricePredict:
	MIN_TRAIN_NUM = 8
	NUM_FEATURE = 3

	"""predict car price.
	train data_set size and scope will also be returned."""
	def predict(self):
		train_X, train_Y, predict_X, i = self._prepare_data(self.series_id, self.model_ids, self.deal_province_id)
		predict_Y = self.linear_regression_method(train_X, train_Y, predict_X)
		return int(predict_Y), len(train_X), i

	"""locally weighted linear regression implemented"""
	def _lwlr(self, train_X, train_Y, predictX):
		if len(train_X) < CarPricePredict.NUM_FEATURE:
			return -1
		return rgr.lwlr(predictX, train_X, train_Y, k=100000000)

	"""predict used car price"""
	def __init__(self, card_month, mileage, series_id, model_ids=None, deal_province_id=None):
		self.card_time = utils.convert_month_to_timestamp(card_month)
		if self.card_time == -1:
			return None
		self.mileage = mileage * 10000
		self.series_id =  series_id
		self.model_ids = model_ids
		self.deal_province_id = deal_province_id
		self.linear_regression_method = self._lwlr

	"""prepare training data_set"""
	def _prepare_data(self, series_id, model_ids=None, deal_province_id=None):
		i = 1
		deal_province_offset = 0
		# try to filter training data by series_id, model_ids and deal_province_id,
		# if training set is not enough, remove deal_province_id constraint
		while i >= 0:
			if (i & (1 << deal_province_id)) > 0:
				tmp_deal_province_id = deal_province_id
			else:
				tmp_deal_province_id = None
			data_set = db.allnet_price(tmp_car_model_ids, tmp_deal_province_id)
			if len(data_set) >= CarPricePredict.MIN_TRAIN_NUM:
				break
			i = i - 1
		# if training set is not enough, return empty training data_set.
		if len(data_set) < CarPricePredict.MIN_TRAIN_NUM: return [], [], [], i

		# filter data
		dataX, dataY = self._filter_data(data_set)
		# if train data_set's size is smaller than feature number, return empty training data_set
		if len(dataX) < CarPricePredict.NUM_FEATURE: return [], [], [], i
		predictX = [[self.card_time, utils.NOW, self.mileage]]
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
		print filtered_data

		# filter point which is far away from predicted mean line
		regr = linear_model.LinearRegression()
		# first NUM_FEATURE columns are feature columns
		dataX = filtered_data[:, :CarPricePredict.NUM_FEATURE]
		# last column is value column
		dataY = filtered_data[:, -1]
		if len(dataX) < CarPricePredict.MIN_TRAIN_NUM:
			return filtered_data
		regr.fit(dataX, dataY)
		distances = dataY - regr.predict(dataX)
		# filter by distance confidence interval
		print len(filtered_data)
		mean, low_confidenc_limit, high_confidence_limit = utils.mean_confidence_interval(distances, confidence=0.99)
		filtered_data = np.array([filtered_data[i] for i in range(len(filtered_data)) if distances[i] >= low_confidenc_limit and distances[i] <= high_confidence_limit])
		print len(filtered_data), mean, low_confidenc_limit, high_confidence_limit

		return filtered_data[:, :CarPricePredict.NUM_FEATURE], filtered_data[:, -1]

