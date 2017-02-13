# -*- coding: UTF-8 -*-

import MySQLdb
import config
import env
import utils
from DBUtils.PooledDB import PooledDB



# connection pool initilization
def init_db_pool(db):
	return PooledDB(MySQLdb, mincached=16, host=config.MYSQL_CONFIG[env.ENV]['host'], user=config.MYSQL_CONFIG[env.ENV]['user'], passwd=config.MYSQL_CONFIG[env.ENV]['passwd'], db=config.MYSQL_CONFIG[env.ENV][db], port=config.MYSQL_CONFIG[env.ENV]['port'], charset="utf8")