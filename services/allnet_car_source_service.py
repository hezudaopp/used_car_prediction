# -*- coding: UTF-8 -*-

import jieba
from datetime import date
import db_wcar
import db_car_type

DICT_FILENAME = "jieba_dict.txt"
jieba.load_userdict(DICT_FILENAME)
# for s in jieba.cut("自动豪华版", cut_all=False):
# 	print s

CUR_YEAR = date.today().year
# suppose that model year is prior to "款" or "年"
MODEL_YEAR_KEYWORDS = (u"款", u"年")
SYNONYMS_KEY_MAP = {u"手自一体":u"自动", "AT":u"自动", "MT":u"手动"}

count = None
def get_count():
	global count
	if count is None:
		count = db_wcar.count_of_allnet_car_source()
	return count

def update_brand_id(page_size=100000):
	size = get_count()
	start = 0
	limit = page_size
	while True:
		print start, size
		if start > size: break
		db_wcar.update_brand_id_of_allnet_car_source(start, limit)
		start = start + limit

def update_series_id(page_size=100000):
	size = get_count()
	start = 0
	limit = page_size
	while True:
		print start, size
		if start > size: break
		db_wcar.update_series_id_of_allnet_car_source(start, limit)
		start = start + limit

empty_model_count = None
def get_empty_model_count():
	global empty_model_count
	if empty_model_count is None:
		empty_model_count = db_wcar.empty_model_count_of_allnet_car_source()
	return empty_model_count

# update empty model id item of allnet_car_source
def update_null_model_id(start=0, page_size=100000):
	size = get_empty_model_count()
	limit = page_size
	while True:
		print start, size
		if start > size: break
		# get empty model id items.
		sale_cars = db_wcar.empty_model_of_allnet_car_source(start, limit)
		for sale_car in sale_cars:
			car_sale_id = sale_car[0]
			series_id = sale_car[1]
			title = sale_car[2]
			model = sale_car[3]

			# try to find model name
			possible_locations = (model, title)
			model_name = ""
			for possible_location in possible_locations:
				if possible_location is not None:
					model_name = model_name + " " + possible_location

			# if model name is empty, continue
			if model_name is None or len(model_name.strip()) == 0:
				continue

			# try to find model year
			model_year = None
			
			for model_year_keyword in MODEL_YEAR_KEYWORDS:
				for possible_location in possible_locations:
					# only if model year have not been found.
					if model_year is not None:
						break
					

					model_year_end_index = possible_location.find(model_year_keyword)
					model_year_start_index = model_year_end_index - 2
					if model_year_start_index >= 0:
						try:
							model_year = int(possible_location[model_year_start_index:model_year_end_index])
							if model_year <= (CUR_YEAR - 2000):
								model_year = model_year + 2000
							else:
								model_year = model_year + 1900
							if model_year < 1970 or model_year > CUR_YEAR:
								model_year = None
						except:
							print "%d Warn: model year, error format." % (car_sale_id)
							model_year = None
			# if model year not found, continue
			if model_year is None:
				continue

			seg_list = jieba.cut(model_name, cut_all=False)
			# put model name's segments into a dict as key, so segments will be unique in a dict.
			keyword_dict = {}
			for seg in seg_list:
				if seg.isspace(): continue
				if seg == '-': continue
				if SYNONYMS_KEY_MAP.has_key(seg):
					seg = SYNONYMS_KEY_MAP[seg]
				# print seg,
				keyword_dict[seg] = True
			# print
			# get models by series id and model year.
			possible_models = db_car_type.car_type_models_of_series_id_and_model_year(series_id, model_year)
			target_model = None
			max_match_count = 0
			for possible_model in possible_models:
				possible_model_name = ""
				if possible_model[1] is not None:
					possible_model_name = possible_model_name + " " + possible_model[1]
				if possible_model[2] is not None:
					possible_model_name = possible_model_name + " " + possible_model[2]
				target_seg_list = jieba.cut(possible_model_name, cut_all=False)
				cur_match_count = 0
				# count how much segments are matched.
				for target_seg in target_seg_list:
					if SYNONYMS_KEY_MAP.has_key(target_seg):
						target_seg = SYNONYMS_KEY_MAP[target_seg]
					# print target_seg,
					if keyword_dict.has_key(target_seg):
						cur_match_count = cur_match_count + 1
				# print
				# set target model to max matched one.
				if cur_match_count > max_match_count and cur_match_count > 1:
					max_match_count = cur_match_count
					target_model = possible_model
			# if target model is found, update model id by primary key.
			if target_model is not None:
				db_wcar.update_model_id_of_allnet_car_source(target_model[0], car_sale_id)
		start = start + limit