# -*- coding: UTF-8 -*-
import json
import os
import sys
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
reload(sys)
sys.setdefaultencoding('utf-8')

from controllers import estimate_controller
import config
from apscheduler.schedulers.background import BackgroundScheduler

# url map
url_map = {
	"/estimate/all_data_regression": estimate_controller.all_data_regression,
	"/estimate/car_series_regression": estimate_controller.car_series_regression,
	"/estimate/replacement_cost_method": estimate_controller.replacement_cost_method,
	"/estimate/get": estimate_controller.get,
}

from services.all_data_regression_service import AllDataRegressionService

# init estimator periodly
def init_all_data_estimator_periodly():
	AllDataRegressionService.init_estimator(True)

# init data.
init_all_data_estimator_periodly()

sched = BackgroundScheduler()
sched.add_job(init_all_data_estimator_periodly, 'cron', day=1, hour=4, minute=5)
sched.start()

# main entrance
def application(env, start_response):
	real_path = env['PATH_INFO']
	try:
		status, result = url_map[real_path](env)
		start_response(str(status), [('Content-Type',' application/json')])
		result = json.dumps(result)
		return [result]
	except:
		return []