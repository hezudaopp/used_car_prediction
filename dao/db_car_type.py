# -*- coding: UTF-8 -*-

import db
import MySQLdb
import re

car_type_pool = db.init_db_pool('car_type')

def car_brand_of_all():
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `id`, `name`
			 FROM `car_brand`
			 WHERE 1 AND `status` = 1"""
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	return results

def car_series_of_all():
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `id`, `name`, `brand_id`, `import_id`, `168_brand_id`
			 FROM `car_series`
			 LEFT JOIN `car_brand_map`
			 ON `car_series`.`brand_id` = `car_brand_map`.`273_brand_id`
			 WHERE 1 AND `car_series`.`status` = 1"""
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	return results

def car_brand_map_insert(car_brand):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """INSERT INTO `car_brand_map`(`273_brand_id`, `273_brand_name`, `168_brand_id`, `168_brand_name`) VALUES (%d, '%s', %d, '%s')""" % (car_brand['273_brand_id'], car_brand['273_brand_name'], car_brand['168_brand_id'], car_brand['168_brand_name'])
	print sql
	result = cursor.execute(sql)
	db.commit()
	cursor.close()
	db.close()

def car_brand_of_168_by_brand_name(brand_name):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT distinct(`brand_id`)
			 FROM `car_series_hedge_rate`
			 WHERE 1 AND `brand_name` = '%s' limit 1""" % (brand_name)
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	return results

def car_series_of_brand_id_of_168(brand_id):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `168_series_id`, `168_series_name`
			 FROM `car_series_168`
			 WHERE 1 AND `168_brand_id` = %d""" % (brand_id)
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	return results

def insert_or_update_car_series_map_of_168(series_id_of_273, series_id_of_168):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """INSERT INTO `car_series_map` (`273_series_id`, `168_series_id`)
	VALUES(%d, %d) 
	ON DUPLICATE KEY UPDATE `168_series_id` = %d""" % (series_id_of_273, series_id_of_168, series_id_of_168)
	result = cursor.execute(sql)
	# utils.debug("update %d's model_id to %d." % (car_sale_id, model_id))
	db.commit()
	cursor.close()
	db.close()
	return result

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
	cursor.close()
	db.close()
	return results

def car_model_of_series_id_and_sale_name(series_id, sale_name):
	db = car_type_pool.connection()
	cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	sql = """SELECT `guide_price`,
		UNIX_TIMESTAMP(STR_TO_DATE(CONCAT(`market_year`, '/', IF(`market_month` > 0, `market_month`, 1), '/1'), '%Y/%m/%d')) AS `market_date`,
		`max_power`, `max_torque`, `max_speed`, `front_track`, `rear_track`
		FROM `car_model`"""
	sql += """WHERE `series_id` = %d AND `sale_name` = '%s' AND `guide_price` > 0
		ORDER BY `model_year` DESC
		LIMIT 0, 1;""" % (series_id, sale_name)
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	if len(results) == 0:
		return None, None
	return results[0]

def car_model_of_id(id):
	db = car_type_pool.connection()
	cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	sql = """SELECT `guide_price`,
		UNIX_TIMESTAMP(STR_TO_DATE(CONCAT(`market_year`, '/', IF(`market_month` > 0, `market_month`, 1), '/1'), '%Y/%m/%d')) AS `market_date`,
		`max_power`, `max_torque`, `max_speed`, `front_track`, `rear_track`
		FROM `car_model`"""
	sql += """WHERE `id` = %d AND `guide_price` > 0
		LIMIT 0, 1;""" % (id)
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	if len(results) == 0:
		return None, None
	return results[0]

def hedge_rates_of(series_id):
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `1st_year`, `2nd_year`, `3rd_year`, `4th_year`, `5th_year`, `6th_year`, `7th_year`, `8th_year`, `9th_year`, `10th_year`
		FROM `car_series_map`
		LEFT JOIN `car_series_hedge_rate` ON `car_series_hedge_rate`.`car_series_id` = `car_series_map`.`168_series_id`
		WHERE `car_series_map`.`273_series_id` = %d
		LIMIT 0, 1;""" % (series_id)
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	if len(results) == 0:
		return None
	return results[0]

def all_hedge_rates():
	db = car_type_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `car_series_map`.`273_series_id`, `1st_year`, `2nd_year`, `3rd_year`, `4th_year`, `5th_year`, `6th_year`, `7th_year`, `8th_year`, `9th_year`, `10th_year`
		FROM `car_series_map`
		LEFT JOIN `car_series_hedge_rate` ON `car_series_hedge_rate`.`car_series_id` = `car_series_map`.`168_series_id`
		WHERE `car_series_map`.`273_series_id` = %d;""" % (series_id)
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	db.close()
	if len(results) == 0:
		return None
	return results