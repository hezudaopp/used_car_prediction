# -*- coding: UTF-8 -*-
import urllib

"""parse url query to dictionary"""
def parse_url_query_to_dict(uwsgi_env):
	query_string = uwsgi_env['QUERY_STRING']
	query_dict = {}
	for query in query_string.split("&"):
		key_value = query.split("=", 1)
		if len(key_value) == 2:
			query_dict[key_value[0]] = urllib.unquote(key_value[1])
		elif len(key_value) == 1:
			query_dict[key_value[0]] = None
	return query_dict