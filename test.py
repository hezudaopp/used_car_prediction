# -*- coding: UTF-8 -*-
from car_price_predict import CarPricePredict

import regression as rgr
import allnet_car_source_service as allnet

DATA = [
		# [167, [289359, 343046], 12, '2014-09', 2.68],
		# [689, [20786, 20794, 31874], 12, '2012-09', 5.2]
		# [644, [1955, 1962, 11478, 11479, 11480, 11481], 12, '2008-07', 9.2],
		# [646, [11542, 11557, 31847, 336580, 325421], 12, '2011-01', 7],
		[815, [629, 7246, 31771], 12, '2011-07', 9.8],
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
ols_y_3 = [82991, 69952, 72673, 51727, 97688, 21314, 91514, 49165, 67096, 150584, 84935, 195109, 137248, 20672, 96636, 55699]
ols_y_2 = [93973, 74787, 91093, 57555, 89788, 27378, 93924, 51789, 75481, 170088, 112273, 206658, 144750, 24135, 111373, 57877]
lwlr_3 = [95761, 76436, 94882, 59169, 90614, 28817, 99952, 53449, 79288, 170585, 111555, 212271, 148134, 25369, 113260, 59623]
lwlr_2 = [96121, 92784, 102414, 89170, 164136, 36752, 79836, 54794, 72932, 163669, 119381, 208276, 137813, 24656, 113956, 71865]

if __name__ == '__main__':
	# predict_Y = []
	# for i in range(len(DATA)):
	# 	car_predict = CarPricePredict(card_month=DATA[i][3], mileage=DATA[i][4], series_id=DATA[i][0], model_ids=DATA[i][1], deal_province_id=DATA[i][2])
	# 	if car_predict is None:
	# 		continue
	# 	result = car_predict.predict()
	# 	print result
	# 	predict_Y.append(result[0])
	# print(rgr.rss_error(DATA_Y, ols_y_3))print
	# print(rgr.rss_error(DATA_Y, ols_y_2))
	# print(rgr.rss_error(DATA_Y, lwlr_3))
	# print(rgr.rss_error(DATA_Y, lwlr_2))

	# allnet.update_brand_id()
	# allnet.update_series_id() # 凯美瑞等车型有可能匹配错误，最好不要更新
	# UPDATE `car_allnet_source` SET series_id = 145 where series_id = 138;
	allnet.update_null_model_id()