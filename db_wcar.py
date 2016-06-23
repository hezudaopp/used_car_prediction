# -*- coding: UTF-8 -*-

import db

wcar_pool = db.init_db_pool('wcar')

# find car source list whose model and model_id is empty.
def empty_model_of_allnet_car_source(start=0, limit=1000):
	db = wcar_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `id`, `series_id`, `title`, `model`
			 FROM `car_allnet_source`
			 WHERE 1 AND `series_id` > 0
			 LIMIT %d, %d""" % (start, limit)
	cursor.execute(sql)
	results = cursor.fetchall()
	db.close()
	return results

# data count of empty model info.
def empty_model_count_of_allnet_car_source():
	db = wcar_pool.connection()
	cursor = db.cursor()
	sql = """SELECT COUNT(1)
			 FROM `car_allnet_source`
			 WHERE 1 AND `series_id` > 0"""
	cursor.execute(sql)
	results = cursor.fetchall()
	db.close()
	return results[0][0]

# update model id by primary key
def update_model_id_of_allnet_car_source(model_id, car_sale_id):
	db = wcar_pool.connection()
	cursor = db.cursor()
	sql = """UPDATE `car_allnet_source` SET `model_id` = %d WHERE `id` = %d""" % (model_id, car_sale_id)
	try:
		cursor.execute(sql)
		# utils.debug("update %d's model_id to %d." % (car_sale_id, model_id))
		db.commit()
	except:
		db.rollback()
	db.close()

# get allnet car source count
def count_of_allnet_car_source():
	db = wcar_pool.connection()
	cursor = db.cursor()
	sql = """SELECT COUNT(*) FROM `car_allnet_source`"""
	cursor.execute(sql)
	results = cursor.fetchall()
	db.close()
	return results[0][0]

# update brand id, map car type's brand id to allnet_source_car's brand id.
def update_brand_id_of_allnet_car_source(start, limit):
	db = wcar_pool.connection()
	cursor = db.cursor()
	affected_rows = None
	sql = """UPDATE wcar.car_allnet_source a
		INNER JOIN
			(SELECT a.id, b.id AS brand_id
			FROM wcar.car_allnet_source a, car_type.car_brand b
			WHERE a.brand = b.name
			LIMIT %d, %d) b
		ON a.id = b.id
		SET a.brand_id = b.brand_id;""" % (start, limit)
	try:
		affected_rows = cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()
	return affected_rows
	

# update series id, map car type's series id to allnet_source_car's series id.
def update_series_id_of_allnet_car_source(start, limit):
	db = wcar_pool.connection()
	cursor = db.cursor()
	affected_rows = None
	sql = """UPDATE wcar.car_allnet_source a
		INNER JOIN
			(SELECT a.id, b.id AS series_id
			FROM wcar.car_allnet_source a, car_type.car_series b
			WHERE a.brand_id = b.brand_id AND a.series = b.name
			LIMIT %d, %d) b
		ON a.id = b.id
		SET a.series_id = b.series_id;""" % (start, limit)
	try:
		affected_rows = cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	db.close()
	return affected_rows

# get car deal data by modelId and deal_province_id
# data's features include card_time, kilometer and price
# def deal_price(model_ids, deal_province_id=None):
# 	db = wcar_pool.connection()
# 	cursor = db.cursor()
# 	sql = "SELECT `card_time`, `deal_time`, `kilometer`, `price`, `deal_price` \
# 			FROM `car_deal_price_evaluate` \
# 			WHERE 1"
# 	model_ids_str = '(' + ', '.join(str(v) for v in model_ids) + ')'
# 	sql += " AND `model_id` in %s" % (model_ids_str)
# 	if deal_province_id != None:
# 		sql += " AND `deal_province_id` = %d" % (deal_province_id)
# 	sql += " AND `price` > 0 AND `deal_price` > 0 AND `card_time` > 0 AND `publish_time` > 0"
# 	sql += " ORDER BY `card_time` ASC"
# 	cursor.execute(sql)
# 	results = cursor.fetchall()
# 	dataSet = []
# 	for row in results:
# 		dataSet.append(map(float, row))
# 	db.close()
# 	return dataSet

def allnet_price(brand_id, series_id, model_id, province_id=None, limit=200):
	db = wcar_pool.connection()
	cursor = db.cursor()
	sql = """SELECT `card_time`, `publish_time`, `kilometer`, `price`
			FROM `car_allnet_source`
			WHERE 1 AND `brand_id` = %d AND `series_id` = %d AND `model_id` = %d""" % (brand_id, series_id, model_id)
	if province_id is not None:
		sql += " AND `province_id` = %d" % (province_id)
	sql += " AND `price` > 0 AND `card_time` > 0 AND `publish_time` > 0"
	sql += " GROUP BY `repeat_id` ORDER BY `publish_time` DESC LIMIT %d" % (limit)
	# print sql
	cursor.execute(sql)
	results = cursor.fetchall()
	dataSet = []
	for row in results:
		dataSet.append(map(float, row))
	db.close()
	return dataSet