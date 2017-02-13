# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn import ensemble
from sklearn.grid_search import GridSearchCV
import threading
import logging

from services import wcar_service
from services import car_type_service
from utils import math_utils
from utils import time_utils
import config
from services.regression_service import RegressionService

"""car price regression of car series

Attribute:
----------
hedge_rates: car series hedge rates list, used to filter unreasonable data.
"""
class CarSeriesRegressionService(RegressionService):
	hedge_rates = None


	@classmethod
	def _init_series_estimator(cls, series_id, province_id):
		# start to init series estimator
		logging.info("init series estimator start")
		# prepare car series hedge rates
		cls.hedge_rates = car_type_service.get_hedge_rates_by_series_id(series_id)

		# prepare train data set
		logging.debug("before prepare data: %f" % time_utils.milli_time())
		cls.data_frame, i = cls._prepare_data(series_id, province_id)
		logging.debug("after prepare data: %f" % time_utils.milli_time())
		if len(cls.data_frame) < config.MIN_TRAIN_NUM:
			cls.est = False
			return

		# split data into train part and test part.
		logging.debug("before train and test data splitting: %f" % time_utils.milli_time())
		X_train, X_test, y_train, y_test = train_test_split(cls.data_frame.drop(['deal_price'], axis=1), cls.data_frame.deal_price, test_size=0.1, random_state=20)
		logging.debug("after train and test data splitting: %f" % time_utils.milli_time())

		# initialize regression method.
		tuned_parameters = {}
		regressor = linear_model.BayesianRidge()
		clf = GridSearchCV(regressor, cv=4, param_grid=tuned_parameters, scoring=cls.loss)
		logging.debug("before fit: %f" % time_utils.milli_time())
		preds = clf.fit(X_train, y_train)
		logging.debug("after fit: %f" % time_utils.milli_time())
		cls.est = clf.best_estimator_

		# calculate test score
		cls.test_score = math_utils.mean_loss_percentage(cls.est.predict(X_test), y_test)
		if cls.test_score > config.MAX_ALLOWED_PERCENTAGE_ERROR: cls.test_score = config.MAX_ALLOWED_PERCENTAGE_ERROR

		logging.info("init series estimator end")

	"""estimate car price"""
	@classmethod
	def estimate(cls, car_deal):
		result = {}

		# init estimator, if failed, return empty result
		cls._init_series_estimator(car_deal.series_id, car_deal.province_id)
		if not cls.est: return result

		# find predict X array
		predict_X = cls.prepare_predict_X(car_deal)
		predict_y = cls.est.predict(predict_X)
		result['price'] = int(predict_y)
		result['min_price'] = int(result['price'] * (1 - cls.test_score))
		result['max_price'] = int(result['price'] * (1 + cls.test_score))
		result['price_c'] = result['price']
		result['min_price_c'] = result['min_price']
		result['max_price_c'] = result['max_price']
		result['predict_method'] = 'linear regression'
		result['test_score'] = cls.test_score
		return result

	"""prepare training data_dict"""
	@classmethod
	def _prepare_data(cls, series_id, province_id):
		i = 1
		deal_province_offset = 0
		# try to filter training data by series_id, sale_name and province_id,
		# if training set is not enough, remove province_id constraint
		while i >= 0:
			if (i & (1 << deal_province_offset)) > 0:
				tmp_province_id = province_id
			else:
				tmp_province_id = None
			data_frame = wcar_service.get_car_deal_data_by_series_id_and_province_id(series_id, tmp_province_id)
			# filter data
			logging.debug("before filtering data: %f" % time_utils.milli_time())
			data_frame = cls.filter_data(data_frame, cls.hedge_rates)
			logging.debug("after filtering data: %f" % time_utils.milli_time())
			if len(data_frame) >= config.MIN_TRAIN_NUM:
				break
			i = i - 1
		# time consuming here
		# logging.debug("before filled blank data: %f" % time_utils.milli_time())
		# data_frame = cls.filled_blank_data(data_frame)
		# logging.debug("after filled blank data: %f" % time_utils.milli_time())
		return data_frame, i