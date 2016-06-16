# -*- coding: UTF-8 -*-

import jieba
from datetime import date
import db

DICT_FILENAME = "jieba_dict.txt"
jieba.load_userdict(DICT_FILENAME)
CUR_YEAR = date.today().year

sale_cars = db.null_model_id_of_allnet_car_source(start=2, limit=2)
for sale_car in sale_cars:
	sale_car_id = sale_car[0]
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
		print sale_car_id, target_model[0]
		db.update_model_id_of_allnet_car_source(target_model[0], sale_car_id)
		pass


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