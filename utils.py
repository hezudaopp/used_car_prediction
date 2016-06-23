# -*- coding: UTF-8 -*-

import time
import datetime
import config
import numpy as np
import scipy as sp
import scipy.stats

NOW = int(time.time())

"""get year info in timestamp"""
def year_of_timestamp(timestamp_in_seconds=None):
	return time.gmtime(timestamp_in_seconds).tm_year

"""get month info in timestamp"""
def month_of_timestamp(timestamp_in_seconds=None):
	return time.gmtime(timestamp_in_seconds).tm_mon

# month fomat example: "2009-06"
# return timestamp in seconds.
# if format error, return -1
def convert_month_to_timestamp(month):
	try:
		return int(time.mktime(datetime.datetime.strptime(month, "%Y-%m").timetuple()))
	except:
		return -1

# compute data's mean confidence interval
# mean difference will also be returned.
def mean_confidence_interval(data, confidence=0.95):
	a = 1.0 * np.array(data)
	n = len(a)
	if n < 1: return -1, -1, -1
	m, se = np.mean(a), scipy.stats.sem(a)
	h = se * sp.stats.t._ppf((1 + confidence) / 2.0, n-1)
	return m, m-h, m+h

def debug(o):
	if config.is_debug:
		if o is None: o = ""
		print "Debug: " + o