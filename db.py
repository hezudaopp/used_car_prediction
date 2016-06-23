# -*- coding: UTF-8 -*-

import MySQLdb
import config
import utils
from DBUtils.PooledDB import PooledDB



# connection pool initilization
def init_db_pool(db):
	return PooledDB(MySQLdb, mincached=16, host=config.MYSQL_CONFIG[config.ENV]['host'], user=config.MYSQL_CONFIG[config.ENV]['user'], passwd=config.MYSQL_CONFIG[config.ENV]['passwd'], db=config.MYSQL_CONFIG[config.ENV][db], port=config.MYSQL_CONFIG[config.ENV]['port'], charset="utf8")