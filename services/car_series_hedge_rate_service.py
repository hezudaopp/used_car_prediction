# -*- coding: UTF-8 -*-

import jieba
import db_car_type
import os


DICT_FILENAME = os.path.join(os.path.split(os.path.realpath(__file__))[0], "jieba_dict.txt")
jieba.load_userdict(DICT_FILENAME)

IMPORT_KEYWORDS = (u"(进口)", u"(海外)")
SYNONYMS_KEY_MAP = {
	u"致炫":u"雅力士",
	"passat":u"帕萨特",
	"tiguan":u"途观",
	"sienna":u"塞纳",
	"mustang":u"野马",
	"hiace":u"海狮",
	"jeep":u"吉普",
	"yeti":u"野帝",
	"aventador":u"埃文塔多",
	"gallardo":u"盖拉多",
	"murcielago":u"蝙蝠",
	"reventon":u"雷文顿",
	"cima":u"西玛",
	"lancer":u"蓝瑟",
	u"阿特兹":"atenza",
	"sportage":u"狮跑",
	"vq":u"威客",
	"superb":u"速派",
	u"赛纳":u"塞纳",
	"enzo":u"恩佐"}

def insert_car_brand_map():
	car_brands = db_car_type.car_brand_of_all()
	for car_brand in car_brands:
		car_brand_dict = {}
		car_brand_dict['273_brand_id'] = car_brand[0]
		car_brand_dict['273_brand_name'] = car_brand[1]

		results = db_car_type.car_brand_of_168_by_brand_name(car_brand_dict['273_brand_name'])
		if len(results) == 0:
			car_brand_dict['168_brand_name'] = ""
			car_brand_dict['168_brand_id'] = 0
		else:
			car_brand_dict['168_brand_name'] = car_brand_dict['273_brand_name']
			car_brand_dict['168_brand_id'] = results[0][0]

		db_car_type.car_brand_map_insert(car_brand_dict)

def insert_car_series_map(start=0, page_size=10000):
	car_series_of_273 = db_car_type.car_series_of_all()
	for car_series in car_series_of_273:
		series_id = car_series[0]
		series_name = car_series[1]
		brand_id = car_series[2]
		import_id = car_series[3]
		brand_id_of_168 = car_series[4]
		if brand_id_of_168 is None: continue

		# split series name multiple pieces
		# update 168 series to series whose series name matched max pieces and total pieces is min.
		series_name = _filter_series_name(series_name)
		seg_list = jieba.cut(series_name, cut_all=False)
		# put series name's segments into a dict as key, so segments will be unique in a dict.
		keyword_dict = {}
		for seg in seg_list:
			if seg.isspace(): continue
			if seg == '-' or seg == '(' or seg == ')' or seg == u'·': continue
			if SYNONYMS_KEY_MAP.has_key(seg):
				seg = SYNONYMS_KEY_MAP[seg]
			keyword_dict[seg] = True

		car_series_of_168 = db_car_type.car_series_of_brand_id_of_168(brand_id_of_168)

		target_series_id = None
		target_series_name = None
		max_match_count = 1
		min_seg_count = 1024
		for target_series in car_series_of_168:
			possible_series_id = target_series[0]
			possible_series_name = target_series[1]
			possible_series_name = _filter_series_name(possible_series_name)
			possible_seg_list = jieba.cut(possible_series_name, cut_all=False)
			cur_match_count = 0
			cur_seg_count = 0
			dismatched = False
			# count how much segments are matched.
			for possible_seg in possible_seg_list:
				if possible_seg.isspace(): continue
				if possible_seg == '-' or possible_seg == '(' or possible_seg == ')' or possible_seg == u'·': continue
				if SYNONYMS_KEY_MAP.has_key(possible_seg):
					possible_seg = SYNONYMS_KEY_MAP[possible_seg]
				if keyword_dict.has_key(possible_seg):
					cur_match_count += 1
				if (possible_seg == u"进口" or possible_seg == u"海外") and import_id == 1:
					cur_match_count += 0.5
				if (possible_seg == u"进口" or possible_seg == u"海外") and import_id != 1:
					dismatched = True
					break
				cur_seg_count += 1
			if dismatched: continue
			# if series_id == 976:
			# 	print cur_match_count, max_match_count, cur_seg_count, min_seg_count
			# set target series to max matched one.
			if (cur_match_count >= max_match_count):
				if cur_match_count == max_match_count and cur_seg_count >= min_seg_count: continue
				max_match_count = cur_match_count
				min_seg_count = cur_seg_count
				target_series_id = possible_series_id
				target_series_name = possible_series_name

		if target_series_id is not None:
			db_car_type.insert_or_update_car_series_map_of_168(series_id, target_series_id)
		print series_id, series_name, import_id,
		print "=>",
		print target_series_name, target_series_id, brand_id_of_168

def _filter_series_name(series_name):
	series_name = series_name.lower()
	series_name = series_name.replace('-', '')
	series_name = series_name.replace(u'级', '')
	series_name = series_name.replace(u'系', '')
	return series_name