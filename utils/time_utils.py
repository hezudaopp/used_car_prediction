# -*- coding: UTF-8 -*-
import re
import time
import datetime

# current timestamp
def now():
	return int(time.time())

def milli_time():
	return time.time()

"""get year info in timestamp"""
def year_of_timestamp(timestamp_in_seconds=None):
	return time.gmtime(timestamp_in_seconds).tm_year

"""get month info in timestamp"""
def month_of_timestamp(timestamp_in_seconds=None):
	return time.gmtime(timestamp_in_seconds).tm_mon

"""months between start time and end"""
def months_between_timestamp(start_timestamp, end_timestamp=None):
	end_year = year_of_timestamp(end_timestamp)
	end_month = month_of_timestamp(end_timestamp)
	start_year = year_of_timestamp(start_timestamp)
	start_month = month_of_timestamp(start_timestamp)
	return ((end_year - start_year) * 12) + (end_month - start_month)

"""month fomat example: "2009-06"
return timestamp in seconds.
if format error, return -1"""
def convert_month_to_timestamp(month):
	try:
		return int(time.mktime(datetime.datetime.strptime(month, "%Y-%m").timetuple()))
	except:
		return -1