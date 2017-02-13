# -*- coding: UTF-8 -*-
import pandas as pd
import re

from dao import db_wcar
from services import car_type_service
from services.regression_service import RegressionService

def get_car_deal_data_by_series_id_and_province_id(series_id, province_id):
	data_dict = db_wcar.car_series_deal_data(series_id, province_id)
	data_frame = RegressionService.process_data(data_dict, car_type_service.CAR_DEAL_FIELDS_SEQUENCE)
	return data_frame

def get_all_car_deal_data():
	data_dict = db_wcar.car_deal_data()
	data_frame = RegressionService.process_data(data_dict, car_type_service.CAR_EVALUATE_FIELDS_SEQUENCE)
	return data_frame