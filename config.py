import env
import logging

VER = 0.3

MYSQL_CONFIG = {
	'local':{
		'host':'127.0.0.1',
		'user':'root',
		'passwd':'',
		'port':3306,
		'wcar':'wcar',
		'car_type':'car_type'
	},
	'test':{
		'host':'192.168.5.31',
		'user':'w273cn',
		'passwd':'w273cn_gototop_0591',
		'port':3306,
		'wcar':'wcar',
		'car_type':'car_type'
	},
	'sim':{
		'host':'192.168.9.111',
		'user':'w273cn',
		'passwd':'w273cn_gototop_0591',
		'port':3306,
		'wcar':'wcar',
		'car_type':'car_type'
	},
	'online':{
		'host':'192.168.9.111',
		'user':'w273cn',
		'passwd':'w273cn_gototop_0591',
		'port':3306,
		'wcar':'wcar',
		'car_type':'car_type'
	}
}

LOGGING_LEVEL = {
	'local':logging.DEBUG,
	'test':logging.DEBUG,
	'sim':logging.WARNING,
	'online':logging.WARNING
}
logging.basicConfig(filename='/var/log/estimate.log', level=LOGGING_LEVEL[env.ENV])

# feature config
MIN_TRAIN_NUM = 50

# used in replacement cost method to determine mileage factor 
MAX_MILES_PER_MONTH = 10000.0

# hedge rate infos
MAX_HEDGE_RATES = [0.8474, 0.7909, 0.7157, 0.6407, 0.5767, 0.4921, 0.4445, 0.4054, 0.3467, 0.2728]
MIN_HEDGE_RATES = [0.5852, 0.4959, 0.4257, 0.3565, 0.2944, 0.2385, 0.1353, 0.0965, 0.0778, 0.0538]
AVG_HEDGE_RATES = [0.7413, 0.6487, 0.5660, 0.4894, 0.4208, 0.3512, 0.2773, 0.2213, 0.1762, 0.1377]


RANDOM_FOREST_REGRESSOR_PICKLE = "random_forest_regressor.pkl"

DEAL_DATA_RELOAD_PERIOD = 2592000.0

MAX_ALLOWED_PERCENTAGE_ERROR = 0.2