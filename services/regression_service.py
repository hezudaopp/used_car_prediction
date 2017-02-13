# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
from sklearn.metrics import make_scorer
import logging

from services import car_type_service
from utils import time_utils
from utils import math_utils

"""Base regression service.

Attributes
----------
est: estimator
test_score: percentage error.

"""
class RegressionService():
	est = None
	test_score = None
	data_frame = None

	loss = make_scorer(math_utils.mean_loss_percentage, greater_is_better=False)

	# prepare predict_X
	@classmethod
	def prepare_predict_X(cls, car_deal, mean_value_dict=None):
		car_model = car_type_service.get_car_model_by_car_deal(car_deal)
		car_model['guide_price'] = cls.process_guide_price(car_model['guide_price'])
		if len(car_model) == 0: return None
		feature_values = [
			car_deal.card_time,
			time_utils.now(),
			car_deal.kilometer
		]
		if mean_value_dict is None:
			feature_values.append(car_model['guide_price'])
			return [feature_values]

		for key in car_type_service.CAR_MODEL_FIELDS_SEQUENCE:
			value = -1
			if key in car_model and car_model[key] is not None:
				float_value = -1
				try:
					float_value = float(car_model[key])
				except ValueError:
					float_value = mean_value_dict[key]
				if float_value > 0:
					value = float_value
			feature_values.append(value)
		return [feature_values]

	# fill blank cell with colume's mean value
	@classmethod
	def filled_blank_data(cls, data_frame):
		for key in car_type_service.CAR_EVALUATE_FIELDS_SEQUENCE:
			if key not in data_frame: continue
			if np.issubdtype(data_frame[key].dtype, np.number): continue
			data_frame[key] = pd.to_numeric(data_frame[key], errors='coerce')
		mean = data_frame.mean(skipna=True, numeric_only=True)
		for key in car_type_service.CAR_EVALUATE_FIELDS_SEQUENCE:
			if key not in data_frame: continue
			if key not in mean: continue
			data_frame[key].fillna(mean[key], inplace=True)
		return data_frame

	# process data: convert all fields to numberic
	@classmethod
	def process_data(cls, data_dict, columns):
		data_frame = pd.DataFrame(data_dict, columns=columns)
		data_frame.guide_price = data_frame.guide_price.apply(cls.process_guide_price)
		data_frame.deal_price = data_frame.deal_price.apply(cls.process_deal_price)
		return data_frame

	"""format guide price field."""
	@classmethod
	def process_guide_price(cls, price):
		if price is None: return -1
		if type(price) == float: return price * 10000
		splitters = "-~"
		price = filter(lambda ch: ch in '0123456789.'+splitters, price)
		for splitter in splitters:
			low_price, splitter, high_price = price.partition(splitter)
			new_price = low_price
			if high_price != '':
				new_price = 0.5 * (float(low_price) + float(high_price))
				break
		try:
			price = float(new_price)
		except ValueError:
			return -1
		return price * 10000

	"""process deal price"""
	@classmethod
	def process_deal_price(cls, price):
		if price is None: return -1
		price = int(price)
		price = price if price < 10000000 else price / 10000
		return price

	"""filter training data_frame, exclude noise"""
	@classmethod
	def filter_data(cls, data_frame, hedge_rates=None):
		# filter cars whose car age is greater than 15 years
		logging.debug("filter by card_time and deal_time")
		data_frame = data_frame[data_frame.card_time > 0]
		data_frame = data_frame[data_frame.deal_time - data_frame.card_time > 0]
		data_frame = data_frame[data_frame.deal_time - data_frame.card_time < 473385600]

		# filter cars whose mileage per month is not in range between 100 and 5000
		logging.debug("filter by mileage")
		data_frame = data_frame[data_frame.kilometer * 25920 / (data_frame.deal_time - data_frame.card_time) > 1]
		data_frame = data_frame[data_frame.kilometer * 25920 / (data_frame.deal_time - data_frame.card_time) < 50]

		logging.debug("filter by guide_price")
		data_frame = data_frame[data_frame.guide_price > 5000]
		data_frame = data_frame[data_frame.guide_price < 10000000]
		# deal price is less than guide price * 90%
		logging.debug("filter by deal_price")
		data_frame = data_frame[data_frame.deal_price > 0.05 * data_frame.guide_price]
		data_frame = data_frame[data_frame.deal_price < 0.9 * data_frame.guide_price]

		logging.debug("filter by car series hedge rates")
		# if deal price should be in car hedge price range
		if hedge_rates is not None and not 0 in hedge_rates:
			usage_years = [min(int(usage_time / 31557600), 8) for usage_time in (data_frame.deal_time - data_frame.card_time)]
			low_hedge_rates = [hedge_rates[usage_year + 2] - 0.05 for usage_year in usage_years]
			data_frame.low_hedge_rates = low_hedge_rates
			data_frame = data_frame[data_frame.deal_price > data_frame.guide_price * data_frame.low_hedge_rates]

			usage_years = [max(min(int(usage_time / 31557600), 10), 1) for usage_time in (data_frame.deal_time - data_frame.card_time)]
			high_hedge_rates = [hedge_rates[usage_year - 1] + 0.05 for usage_year in usage_years]
			data_frame.high_hedge_rates = high_hedge_rates
			data_frame = data_frame[data_frame.deal_price < data_frame.guide_price * data_frame.high_hedge_rates]

		logging.debug("filter completed")
		return data_frame