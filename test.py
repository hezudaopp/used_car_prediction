# -*- coding: UTF-8 -*-
from car_price_predict import CarPricePredict

import regression as rgr
# import allnet_car_source_service as allnet

DATA = [
		[131, 1164, 289359, 12, '2014-09', 2.68],
		[86, 689, 20786, 12, '2012-09', 5.2],
		[84, 644, 1955, 12, '2008-07', 9.2],
		[84, 646, 11542, 12, '2011-01', 7],
		[98, 815, 629, 12, '2011-07', 9.8],
		[98, 821, 324563, 39, '2010-04', 8],
		[53, 376, 1693, 12, '2012-12', 5],
		[31, 244, 2765, 12, '2011-05', 6.8],
		[18, 102, 290320, 12, '2012-02', 7],
		[66, 2117, 23571, 12, '2012-09', 9.9],
		[82, 595, 286557, 13, '2014-06', 2.6],
		[60, 433, 23358, 53, '2014-04', 3.6],
		[60, 433, 23358, 53, '2010-01', 5.6],
		[89, 736, 1830, 18, '2010-12', 7],
		[136, 1247, 352963, 18, '2015-02', 2.3],
		[86, 684, 872, 18, '2010-06', 4.8],

		# [131, 1164, [289359, 343046], 12, '2014-09', 2.68],
		# [689, [20786, 20794, 31874], 12, '2012-09', 5.2]
		# [644, [1955, 1962, 11478, 11479, 11480, 11481], 12, '2008-07', 9.2],
		# [646, [11542, 11557, 31847, 336580, 325421], 12, '2011-01', 7],
		# [98, 815, [629, 7246, 31771], 12, '2011-07', 9.8],
		# [821, [324563], 39, '2010-04', 8],
		# [376, [1693, 30644, 337482, 326812, 326810], 12, '2012-12', 5],
		# [244, [2765, 2779, 13541, 32835], 12, '2011-05', 6.8],
		# [102, [290320, 290365, 342052, 342047], 12, '2012-02', 7],
		# [2117, [23571, 23572], 12, '2012-09', 9.9],
		# [595, [286557, 341564, 333222], 13, '2014-06', 2.6],
		# [433, [23358, 30321, 332644], 53, '2014-04', 3.6],
		# [433, [23358, 30321, 332644], 53, '2010-01', 5.6],
		# [736, [1830, 11114, 31807, 332559], 18, '2010-12', 7],
		# [1247, [352963, 353283], 18, '2015-02', 2.3],
		# [684, [872, 8164], 18, '2010-06', 4.8],
	]

DATA_Y = [117000, 62000, 95000, 63000, 90000, 33000, 68000, 48000, 75000, 168000, 120000, 280000, 110000, 18000, 110000, 54000]

if __name__ == '__main__':
	predict_Y = []
	for i in range(len(DATA)):
		data = DATA[i]
		car_predict = CarPricePredict(data[0], data[1], data[2], data[3], data[4], data[5])
		result = int(car_predict.predict_by_replacement_cost_method())
		predict_Y.append(result)
		print result,
	print(rgr.rss_error(DATA_Y, predict_Y))

	# for i in range(len(DATA)):
	# 	data = DATA[i]
	# 	car_predict = CarPricePredict(data[0], data[1], data[2], data[3], data[4], data[5])
	# 	if car_predict is None:
	# 		continue
	# 	result = car_predict.predict()
	# 	print result
	# 	predict_Y.append(result[0])
	# print(rgr.rss_error(DATA_Y, predict_Y))

	# allnet.update_brand_id()
	# allnet.update_series_id() # 凯美瑞等车型有可能匹配错误，最好不要更新
	# UPDATE `car_allnet_source` SET series_id = 145 where series_id = 138;
	# ALTER TABLE `car_allnet_source` ADD INDEX `brand_series_model` (`brand_id`, `series_id`, `model_id`) USING BTREE ;
	# allnet.update_null_model_id()