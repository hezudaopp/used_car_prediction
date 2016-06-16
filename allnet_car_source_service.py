# -*- coding: UTF-8 -*-

import jieba
from datetime import date
import db

DICT_FILENAME = "jieba_dict.txt"
jieba.load_userdict(DICT_FILENAME)

CUR_YEAR = date.today().year

count = None
def get_count():
	global count
	if count is None:
		count = db.count_of_allnet_car_source()
	return count

def update_brand_id(page_size=100000):
	size = get_count()
	start = 0
	limit = page_size
	while True:
		print start, size
		if start > size: break
		db.update_brand_id_of_allnet_car_source(start, limit)
		start = start + limit

def update_series_id(page_size=100000):
	size = get_count()
	start = 0
	limit = page_size
	while True:
		print start, size
		if start > size: break
		db.update_series_id_of_allnet_car_source(start, limit)
		start = start + limit

empty_model_count = None
def get_empty_model_count():
	global empty_model_count
	if empty_model_count is None:
		empty_model_count = db.empty_model_count_of_allnet_car_source()
	return empty_model_count

def update_null_model_id(page_size=100000):
	size = get_empty_model_count()
	start = 0
	limit = page_size
	while True:
		print start, size
		if start > size: break
		sale_cars = db.empty_model_of_allnet_car_source(start, limit)
		for sale_car in sale_cars:
			car_sale_id = sale_car[0]
			series_id = sale_car[1]
			title = sale_car[2]
			model_name = sale_car[3]
			seg_list = jieba.cut(model_name, cut_all=False)
			model_year = None
			i = 0
			keyword_dict = {}
			for seg in seg_list:
				if seg.isspace(): continue
				if i == 0:
					try:
						seg = int(seg)
						if seg > 1989 and seg <= CUR_YEAR:
							model_year = seg
					except:
						continue
				keyword_dict[seg] = True
				i = i + 1
			if model_year is None: continue
			possible_models = db.car_type_models_of_series_id_and_model_year(series_id, model_year)
			target_model = None
			max_match_count = 0
			for possible_model in possible_models:
				target_seg_list = jieba.cut(possible_model[1], cut_all=False)
				cur_match_count = 0
				for target_seg in target_seg_list:
					if keyword_dict.has_key(target_seg):
						cur_match_count = cur_match_count + 1
				if cur_match_count > max_match_count and cur_match_count >= 2:
					max_match_count = cur_match_count
					target_model = possible_model
			if target_model is not None:
				db.update_model_id_of_allnet_car_source(target_model[0], car_sale_id)
		start = start + limit


# seg_list = jieba.cut("2011款0.8手动冠军版惠民补贴", cut_all=False)
# year = date.today().year
# model_year = None
# i = 0
# for seg in seg_list:
# 	if i == 0:
# 		seg = int(seg)
# 		if seg > 1989 and seg <= year:
# 			model_year = seg

# 	i = i + 1