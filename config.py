ENV = 'local'

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
		'host':'192.168.5.32',
		'user':'tangwj_tmp',
		'passwd':'asdfjwier08',
		'port':3307,
		'wcar':'tangwj_tmp',
		'car_type':'car_type'
	}
}

is_debug = False
if ENV == "local" or ENV == "test":
	is_debug = True