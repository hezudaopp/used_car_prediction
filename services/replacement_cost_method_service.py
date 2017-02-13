# -*- coding: UTF-8 -*-
import math

from utils import time_utils
from services import car_type_service
from services.regression_service import RegressionService
import config

CONDITION_BAD = 0
CONDITION_NORMAL = 1
CONDITION_GOOD = 2
CAR_LIFE_MONTHS = 180

"""estimate car price by replacement cost method"""
def estimate(car_deal):
	result = {}
	car_model = car_type_service.get_car_model_by_car_deal(car_deal)
	if len(car_model) == 0: return result
	guide_price = RegressionService.process_guide_price(car_model['guide_price'])
	# purchase_price = guide_price + ((guide_price / 1.17) * purchase_tax_rate)
	guide_price_adjustment_factor = 1 + 0.01 * (-5 * math.log10(guide_price / 10000) + 10)
	purchase_price = guide_price * guide_price_adjustment_factor
	car_usage_months = time_utils.months_between_timestamp(car_deal.card_time)
	# if car's age is less than 1 month or greater than 10 years,
	# its hedge rate info is empty, so return empty list in that condition.
	if car_usage_months > CAR_LIFE_MONTHS or car_usage_months < 1: return result
	# get car ten years' hedge rate
	hedge_rates = car_type_service.get_hedge_rates_by_series_id(car_deal.series_id)
	if hedge_rates is None: return result

	diff_years = int(car_usage_months / 12)
	diff_months = None
	last_year_hedge_rate = None
	this_year_hedge_rate = None
	left_diff_months = None
	# if car usage year is less than ten years
	if diff_years < 10:
		left_diff_months = 12
		diff_months = int(car_usage_months % left_diff_months)
		# calculate last year's hedge rate.
		# if car's year is less than 1, last year's hedge rate equals to 1.
		last_year_hedge_rate = hedge_rates[0]
		if diff_years > 0:
			last_year_hedge_rate = hedge_rates[diff_years - 1]
		this_year_hedge_rate = hedge_rates[diff_years]
	else:
		left_diff_months = 60
		diff_months = car_usage_months - CAR_LIFE_MONTHS + left_diff_months
		last_year_hedge_rate = hedge_rates[9]
		this_year_hedge_rate = 0.01
	
	if last_year_hedge_rate == 0: last_year_hedge_rate = None
	if this_year_hedge_rate == 0: this_year_hedge_rate = None
	# if hedge rate is None, return empty list
	if last_year_hedge_rate is None or this_year_hedge_rate is None: return result
	if last_year_hedge_rate < this_year_hedge_rate: return result
	# suppose that hedge rate between last year and this year follow linear degression rule.
	cur_hedge_rate = last_year_hedge_rate - ((last_year_hedge_rate - this_year_hedge_rate) * diff_months / left_diff_months)
	result['price'] = int(purchase_price * cur_hedge_rate * mileage_factor(car_deal.kilometer, car_usage_months))
	result['min_price'] = int(result['price'] * condition_factor(CONDITION_BAD))
	result['max_price'] = int(result['price'] * condition_factor(CONDITION_GOOD))
	result['price_c'] = result['price']
	result['min_price_c'] = result['min_price']
	result['max_price_c'] = result['max_price']
	result['predict_method'] = 'replacement cost method'
	result['test_score'] = None
	return result

"""mileage adjustment factor"""
def mileage_factor(kilometer, car_usage_months):
	kilometer_per_month = kilometer / car_usage_months
	score = 1.0 - kilometer_per_month / config.MAX_MILES_PER_MONTH
	if score < 0: score = 0
	return score * 0.3 + 0.7

"""car condition adjustment factor"""
def condition_factor(condition):
	condition_weight = 0.06
	return (1 - condition_weight) + (condition_weight * condition)