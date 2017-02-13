# -*- coding: UTF-8 -*-
from dao import db_car_type
from utils import math_utils

CAR_DEAL_FIELDS_SEQUENCE = ('card_time', 'deal_time', 'kilometer', 'guide_price', 'deal_price')
CAR_MODEL_FIELDS_SEQUENCE = ('guide_price', 'market_date', 'max_power', 'max_torque', 'max_speed', 'front_track', 'rear_track')
CAR_EVALUATE_FIELDS_SEQUENCE = ('card_time', 'deal_time', 'kilometer', 'guide_price', 'market_date', 'max_power', 'max_torque', 'max_speed', 'front_track', 'rear_track', 'deal_price')

# car model info by model id or series id & sale name
def get_car_model_by_car_deal(car_deal):
	if car_deal.model_id is None:
		return db_car_type.car_model_of_series_id_and_sale_name(car_deal.series_id, car_deal.sale_name)
	return db_car_type.car_model_of_id(car_deal.model_id)

# car series hedge rates list.
# 0.01 is appended to last of the list as a boundary
def get_hedge_rates_by_series_id(series_id):
	hedge_rates = db_car_type.hedge_rates_of(series_id)
	if hedge_rates is None: return hedge_rates
	hedge_rates = [math_utils.percentage_to_float(hedge_rate) for hedge_rate in hedge_rates]
	hedge_rates.append(0.01)
	return hedge_rates

# hedge rates dict
# key: series id
# value: series hedge rate list.
def get_hedge_rates_dict():
	hedge_rates = db_car_type.hedge_rates_of()
	hedge_rates_dict = {}
	for hedge_rate in hedge_rates:
		hedge_rates_dict[hedge_rate[0]] = hedge_rate[1:]
	return hedge_rates_dict