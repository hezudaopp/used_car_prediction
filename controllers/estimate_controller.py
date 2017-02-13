from services import car_series_regression_service
from services import replacement_cost_method_service
from services import all_data_regression_service
from models.car_deal import CarDeal
from utils import string_utils
from utils import time_utils
import config

# predict car price based on car deal data of some series.
# this method will be more accurate
def car_series_regression(uwsgi_env):
	car_deal, err_msg = validate_and_get_car_deal(uwsgi_env)
	if car_deal is None:
		return 400, err_msg
	return 200, car_series_regression_service.CarSeriesRegressionService.estimate(car_deal)

# predict car price using replacement cost method.
def replacement_cost_method(uwsgi_env):
	car_deal, err_msg = validate_and_get_car_deal(uwsgi_env)
	if car_deal is None:
		return 400, err_msg
	return 200, replacement_cost_method_service.estimate(car_deal)

# predict car price based on all car deal data.
def all_data_regression(uwsgi_env):
	car_deal, err_msg = validate_and_get_car_deal(uwsgi_env)
	if car_deal is None:
		return 400, err_msg
	return 200, all_data_regression_service.AllDataRegressionService.estimate(car_deal)

# entrance of car price prediction.
def get(uwsgi_env):
	car_deal, err_msg = validate_and_get_car_deal(uwsgi_env)
	if car_deal is None:
		return 400, err_msg
	# learn by car series data
	result = car_series_regression_service.CarSeriesRegressionService.estimate(car_deal)
	if 'price' in result: return 200, result

	# replacement cost method
	result = replacement_cost_method_service.estimate(car_deal)
	if 'price' in result: return 200, result

	# if car series estimation does not return a result.
	# estimate all car deal data estimation.
	result = all_data_regression_service.AllDataRegressionService.estimate(car_deal)
	if 'price' in result: return 200, result

	return 200, result

# retrieve paramaters from context
# valiate parameters and then parse parameters to dict
def validate_and_get_car_deal(uwsgi_env):
	query_dict = string_utils.parse_url_query_to_dict(uwsgi_env)
	# check whether required key is disappeared.
	required_keys = ("series_id", "sale_name", "car_time", "kilometer", "province_id")
	for required_key in required_keys:
		if required_key not in query_dict:
			return None, {"err_msg": "Invalid argument: " + required_key}
	if int(query_dict["car_time"]) > time_utils.now():
		return None, {"err_msg": "Invalid argument: car_time"}
	car_deal = CarDeal(query_dict)
	return car_deal, None