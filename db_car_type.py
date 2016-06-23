# -*- coding: UTF-8 -*-

import db
import re

car_type_pool = db.init_db_pool('car_type')

# find car type models by series id and model year
def car_type_models_of_series_id_and_model_year(series_id, model_year):
	db = car_type_pool.connection()
	cursor = db.cursor()
	model_years = (model_year, model_year+1, model_year-1)
	for year in model_years:
		sql = """SELECT `id`, `model_name`, `sale_name`, `produce_year`
			FROM `car_model`
			WHERE 1 AND `series_id` = %d AND `model_year` = %d AND `status`=1
			GROUP BY `sale_name`
			ORDER BY `id` ASC""" % (series_id, year)
		cursor.execute(sql)
		results = cursor.fetchall()
		if len(results) > 0:
			break
	# duplicated sale name will be ignored.
	# sale_name_dict = {}
	# for result in results:
	# 	if not sale_name_dict.has_key(result[1]):
	# 		sale_name_dict[result[1]] = result
	# results = tuple(sale_name_dict.values())
	db.close()
	return results

# price of car model
def price_of_car_model(model_id):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `guide_price`
			FROM `car_model`
			WHERE 1 AND `id` = %d""" % (model_id)
	cursor.execute(sql)
	results = cursor.fetchall()
	if len(results) == 0:
		return -1
	price = float(re.search(r'[\d\.]+', results[0][0]).group()) * 10000
	db.close()
	return price

# price of replacement car model
def price_of_replacement_car_model(series_id, model_id):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `b`.`guide_price`, `b`.`model_year` FROM `car_model` `a`,
		(SELECT `id`, `sale_name`, `guide_price`, `model_year` FROM `car_model` WHERE `series_id` = %d) `b`
		WHERE `a`.`series_id` = %d and `a`.`id` = %d and `a`.`sale_name` = `b`.`sale_name`
		ORDER BY `model_year` DESC
		LIMIT 0, 1;""" % (series_id, series_id, model_id)
	cursor.execute(sql)
	results = cursor.fetchall()
	if len(results) == 0:
		return -1
	price = float(re.search(r'[\d\.]+', results[0][0]).group()) * 10000
	db.close()
	return price