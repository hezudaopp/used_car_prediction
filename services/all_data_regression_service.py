# -*- coding: UTF-8 -*-

import config
from services import car_type_service
from services import wcar_service
from services.regression_service import RegressionService
from utils import math_utils

from sklearn.cross_validation import train_test_split
from sklearn import ensemble
from sklearn.grid_search import GridSearchCV
import numpy as np
import logging

class AllDataRegressionService(RegressionService):
	"""preload estimator"""
	@classmethod
	def init_estimator(cls, reload=False):
		if cls.est is not None and reload == False: return
		logging.info("init all deal data estimator start")
		cls.data_frame = wcar_service.get_all_car_deal_data()
		cls.data_frame = cls.filter_data(cls.data_frame)
		cls.data_frame = cls.filled_blank_data(cls.data_frame)

		# split data into train part and test part.
		X_train, X_test, y_train, y_test = train_test_split(cls.data_frame.drop(['deal_price'], axis=1), cls.data_frame.deal_price, test_size=0.2, random_state=42)
		# tuned_parameters = {'n_estimators': [100], 'max_depth': [4], 'min_samples_split': [1], 'learning_rate': [0.01], 'loss': ['lad']}
		# regressor = ensemble.GradientBoostingRegressor()
		tuned_parameters = {'n_estimators': [40], 'random_state': [22]}
		regressor = ensemble.RandomForestRegressor()
		clf = GridSearchCV(regressor, cv=4, param_grid=tuned_parameters, scoring=cls.loss)
		preds = clf.fit(X_train, y_train)
		cls.est = clf.best_estimator_
		cls.test_score = math_utils.mean_loss_percentage(cls.est.predict(X_test), y_test)
		if cls.test_score > config.MAX_ALLOWED_PERCENTAGE_ERROR: cls.test_score = config.MAX_ALLOWED_PERCENTAGE_ERROR

		logging.info("init all deal data estimator end")

	"""estimate car price"""
	@classmethod
	def estimate(cls, car_deal):
		cls.init_estimator()
		result = {}
		# find predict X array
		predict_X = cls.prepare_predict_X(car_deal, cls.data_frame.mean())
		predict_y = cls.est.predict(predict_X)
		result['price'] = int(predict_y)
		result['min_price'] = int(result['price'] * (1 - cls.test_score))
		result['max_price'] = int(result['price'] * (1 + cls.test_score))
		result['price_c'] = result['price']
		result['min_price_c'] = result['min_price']
		result['max_price_c'] = result['max_price']
		result['predict_method'] = 'random forest regression'
		result['test_score'] = cls.test_score
		return result
