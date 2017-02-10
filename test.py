# -*- coding: UTF-8 -*-

from services import regression_service
from services import wcar_service
from services.all_data_regression_service import AllDataRegressionService
from services.car_series_regression_service import CarSeriesRegressionService
from services import replacement_cost_method_service
from models.car_deal import CarDeal
import os
import sys
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
import datetime

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import ensemble
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle

# AllDataRegressionService.init_estimator()
# X_test = AllDataRegressionService.X_test
# y_test = AllDataRegressionService.y_test
# print np.mean(np.abs((AllDataRegressionService.est.predict(X_test) - y_test) / y_test))

# import threading

# def hello(name):
#     print "hello %s\n" % name

#     global timer
#     timer = threading.Timer(2.0, hello, ["Hawk"])
#     timer.start()

# if __name__ == "__main__":
# 	hello("one")


# from scipy.stats import pearsonr
# np.random.seed(0)
# size = 300
# x = np.random.normal(0, 1, size)
# print "Lower noise", pearsonr(x, x + np.random.normal(0, 1, size))
# print "Higher noise", pearsonr(x, x + np.random.normal(0, 10, size))



# features selection by random forest
# from sklearn.cross_validation import cross_val_score, ShuffleSplit
# from sklearn.datasets import load_boston
# from sklearn.ensemble import RandomForestRegressor

# AllDataRegressionService.init_data_frame()

# X = AllDataRegressionService.data_frame.drop(['deal_price'], axis=1).as_matrix()
# Y = AllDataRegressionService.data_frame.deal_price.tolist()
# names = AllDataRegressionService.data_frame.columns.values.tolist()


# scores = []
# for i in range(X.shape[1]):
#      score = cross_val_score(rf, X[:, i:i+1], Y, scoring="r2",
#                               cv=ShuffleSplit(len(X), 3, .1))
#      scores.append((round(np.mean(score), 3), names[i]))
# print sorted(scores, reverse=True)

# rf = RandomForestRegressor(n_estimators=50, random_state=22)
# X_train, X_test, y_train, y_test = train_test_split(AllDataRegressionService.data_frame.drop(['deal_price'], axis=1), AllDataRegressionService.data_frame.deal_price, test_size=0.01)
# rf.fit(X_train, y_train)
# sorted_idx = np.argsort(rf.feature_importances_)
# print X_train.columns[sorted_idx]
# print rf.feature_importances_[sorted_idx]



# print 1
# data_frame = wcar_service.get_all_car_deal_data()
# print 2
# data_frame = regression_service.filled_blank_data(data_frame)
# data_frame.to_csv('deal_price.csv')
# print 3
# # split data into train part and test part.
# X_train, X_test, y_train, y_test = train_test_split(data_frame.drop(['deal_price'], axis=1), data_frame.deal_price, test_size=0.2, random_state=20)
# print 4, len(X_train)
# RANDOM_FOREST_REGRESSOR = ensemble.RandomForestRegressor(n_estimators=10, n_jobs=-1)
# RANDOM_FOREST_REGRESSOR.fit(X_train, y_train)
# print 5
# filename = 'random_forest_regressor.pkl'
# with open(filename, 'w') as file: # open file with write-mode
#     pickle.dump(RANDOM_FOREST_REGRESSOR, file) # serialize and save object
# print 6

# data = pd.read_csv("deal_data.csv")
# X_train, X_test, y_train, y_test = train_test_split(data.drop(['deal_price'], axis=1), data.deal_price, test_size=0.2, random_state=datetime.datetime.now().microsecond)
# print len(X_train)

# est = ensemble.RandomForestRegressor(n_estimators=10, n_jobs=-1)
# est.fit(X_train, y_train)
# print est.score(X_test, y_test)

# fn = 'random_forest_regressor.pkl'
# with open(fn, 'w') as f: # open file with write-mode
#     pickle.dump(est, f) # serialize and save object

# new_est = None
# with open(fn, 'r') as f:
#     new_est = pickle.load(f)   # read file and build object
# if new_est is None: exit()
# print new_est.score(X_test, y_test)

# # figure to determine which features are most important
# feature_importance = new_est.feature_importances_
# feature_importance = 100.0 * (feature_importance / feature_importance.max())
# sorted_idx = np.argsort(feature_importance)
# pos = np.arange(sorted_idx.shape[0]) + .5
# pvals = feature_importance[sorted_idx]
# pcols = X_train.columns[sorted_idx]
# plt.figure(figsize=(8,12))
# plt.barh(pos, pvals, align='center')
# plt.yticks(pos, pcols)
# plt.xlabel('Relative Importance')
# plt.title('Variable Importance')
# plt.show()

# grid search
# n_est = 400
# tuned_parameters = {
# 	"n_estimators": [ n_est ],
# 	"max_depth" : [ 4 ],
# 	"learning_rate": [ 0.01 ],
# 	"min_samples_split" : [ 1 ],
# 	"loss" : [ 'ls', 'lad' ]
# }
# gbr = ensemble.GradientBoostingRegressor()
# est = GridSearchCV(gbr, cv=3, param_grid=tuned_parameters,
# 		scoring='median_absolute_error')
# est.fit(X_train, y_train)
# best = est.best_estimator_
# 

tests = [
	{"series_id":379, "sale_name":"1.6 手自一体 Sporty", "model_year":2009, "car_time":1272643200, "kilometer":47200, "province_id":12, "city_id":1},
	{"series_id":650, "sale_name":"2.4 手自一体 豪华版", "model_year":2012, "car_time":1359648000, "kilometer":46200, "province_id":12, "city_id":1},
	{"series_id":379, "sale_name":"1.6 手自一体 舒适版", "model_year":2014, "car_time":1446307200, "kilometer":7000, "province_id":12, "city_id":1},
	{"series_id":503, "sale_name":"2.0 手自一体 时尚型", "model_year":2011, "car_time":1328025600, "kilometer":36900, "province_id":12, "city_id":1},
	{"series_id":923, "sale_name":"2.2T 手自一体 两驱锋芒进化版智慧型", "model_year":2013, "car_time":1380556800, "kilometer":80800, "province_id":12, "city_id":1},
	{"series_id":242, "sale_name":"2.4SIDI 手自一体 雅致版", "model_year":2012, "car_time":1364745600, "kilometer":49800, "province_id":12, "city_id":1},
	{"series_id":376, "sale_name":"1.4TSI 双离合 技术版", "model_year":2010, "car_time":1264953600, "kilometer":107900, "province_id":12, "city_id":1},
	{"series_id":1164, "sale_name":"1.6T 手自一体 SL舒适版", "model_year":2013, "car_time":1388505600, "kilometer":41200, "province_id":12, "city_id":1},
	{"series_id":504, "sale_name":"3.0 手自一体 领先型", "model_year":2008, "car_time":1212249600, "kilometer":90400, "province_id":12, "city_id":1},
	{"series_id":420, "sale_name":"1.5 手动 标准版", "model_year":2009, "car_time":1259596800, "kilometer":104100, "province_id":12, "city_id":1},
	{"series_id":906, "sale_name":"1.8 手动 基本型", "model_year":2012, "car_time":1354291200, "kilometer":58700, "province_id":12, "city_id":1},
	{"series_id":400, "sale_name":"3.6 手自一体 V6 4座加长行政版", "model_year":2009, "car_time":1280592000, "kilometer":59000, "province_id":12, "city_id":1},
	{"series_id":2324, "sale_name":"1.6 手动 豪华版", "model_year":2014, "car_time":1406822400, "kilometer":61500, "province_id":12, "city_id":1},
	{"series_id":248, "sale_name":"1.6 手自一体 时尚版", "model_year":2012, "car_time":1341072000, "kilometer":50000, "province_id":12, "city_id":1},
	{"series_id":2023, "sale_name":"2.0T 双离合 旗舰运动型", "model_year":2012, "car_time":1354291200, "kilometer":90000, "province_id":12, "city_id":1},
	{"series_id":643, "sale_name":"2.4 自动 VTI-S NAVI尊贵导航版", "model_year":2013, "car_time":1375286400, "kilometer":50000, "province_id":12, "city_id":1},
	{"series_id":105, "sale_name":"2.5 手自一体 S 舒适版", "model_year":2009, "car_time":1257004800, "kilometer":80000, "province_id":12, "city_id":1},
	{"series_id":15, "sale_name":"1.6 手自一体 限量版II", "model_year":2013, "car_time":1412092800, "kilometer":14000, "province_id":12, "city_id":1}
]

for test in tests:
	# test = tests[11]
	car_deal = CarDeal(test)
	result = AllDataRegressionService.estimate(car_deal)
	# result = CarSeriesRegressionService.estimate(car_deal)
	# result = replacement_cost_method_service.estimate(car_deal)
	if 'price' in result:
		print result['price'], result['test_score']
	else:
		print

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.cross_validation import train_test_split
# from sklearn.datasets import load_boston


# # Create a random dataset
# boston = load_boston()
# X = boston.data
# y = boston.target

# X_train, X_test, y_train, y_test = train_test_split(X, y,
#                                                     train_size=400,
#                                                     random_state=4)

# regr_rf = RandomForestRegressor(n_estimators=30, max_depth=30, random_state=3, min_samples_leaf=1)
# regr_rf.fit(X_train, y_train)

# # Predict on new data
# y_rf = regr_rf.predict(X_test)
# print y_test, y_rf

# # Plot the results
# plt.figure()
# s = 50
# a = 0.4
# plt.scatter(y_test, y_rf,
#             c="c", s=s, marker="^", alpha=a,
#             label="RF score=%.2f" % regr_rf.score(X_test, y_test))
# plt.xlim([0, 60])
# plt.ylim([0, 60])
# plt.xlabel("target 1")
# plt.ylabel("target 2")
# plt.title("random forests")
# plt.legend()
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
 
# plt.figure(1) # 创建图表1
# plt.figure(2) # 创建图表2
# ax1 = plt.subplot(211) # 在图表2中创建子图1
# ax2 = plt.subplot(212) # 在图表2中创建子图2
 
# x = np.linspace(0, 3, 100)
# for i in xrange(5):
#     plt.figure(1)  #❶ # 选择图表1
#     plt.plot(x, np.exp(i*x/3))
#     plt.sca(ax1)   #❷ # 选择图表2的子图1
#     plt.plot(x, np.sin(i*x))
#     plt.sca(ax2)  # 选择图表2的子图2
#     plt.plot(x, np.cos(i*x))
 
# plt.show()
# 

# """estimate deal price by linear model"""
# def linear_regression(data, predict_X):
	
	# bayesian ridge
	# est = linear_model.BayesianRidge()
	# est.fit(X_train, y_train)
	# err = metrics.median_absolute_error(y_test, est.predict(X_test))
	# return est.predict(predict_X)[0], err

	# estimate by linear models
	# ests = [linear_model.LinearRegression(),
	# linear_model.Ridge(),
	# linear_model.Lasso(),
	# linear_model.ElasticNet(),
	# linear_model.BayesianRidge(),
	# linear_model.OrthogonalMatchingPursuit()]
	# ests_labels = np.array(['Linear', 'Ridge', 'Lasso', 'ElasticNet', 'BayesRidge', 'OMP'])
	# errvals = np.array([])
	# for est in ests:
	# 	est.fit(X_train, y_train)
	# 	this_err = metrics.median_absolute_error(y_test, est.predict(X_test))
	# 	#print "got error %0.2f" % this_err
	# 	errvals = np.append(errvals, this_err)

	# compare different linear models with figure
	# pos = np.arange(errvals.shape[0])
	# srt = np.argsort(errvals)
	# plt.figure(figsize=(7,5))
	# plt.bar(pos, errvals[srt], align='center')
	# plt.xticks(pos, ests_labels[srt])
	# plt.xlabel('Estimator')
	# plt.ylabel('Median Absolute Error')
	# plt.show()
	
	# grid search
	# n_est = 400
	# tuned_parameters = {
	# 	"n_estimators": [ n_est ],
	# 	"max_depth" : [ 4 ],
	# 	"learning_rate": [ 0.01 ],
	# 	"min_samples_split" : [ 1 ],
	# 	"loss" : [ 'ls', 'lad' ]
	# }
	# gbr = ensemble.GradientBoostingRegressor()
	# est = GridSearchCV(gbr, cv=3, param_grid=tuned_parameters,
	# 		scoring='median_absolute_error')
	# preds = est.fit(X_train, y_train)
	# best = est.best_estimator_

	# plot error for each round of boosting, this figure can help us determining n_est argument.
	# test_score = np.zeros(n_est, dtype=np.float64)
	# train_score = best.train_score_
	# for i, y_pred in enumerate(best.staged_predict(X_test)):
	# 	test_score[i] = best.loss_(y_test, y_pred)
	# plt.figure(figsize=(12, 6))
	# plt.subplot(1, 2, 1)
	# plt.plot(np.arange(n_est), train_score, 'darkblue', label='Training Set Error')
	# plt.plot(np.arange(n_est), test_score, 'red', label='Test Set Error')
	# plt.legend(loc='upper right')
	# plt.xlabel('Boosting Iterations')
	# plt.ylabel('Least Absolute Deviation')
	# plt.show()

	# figure to determine which features are most important
	# feature_importance = est.best_estimator_.feature_importances_
	# feature_importance = 100.0 * (feature_importance / feature_importance.max())
	# sorted_idx = np.argsort(feature_importance)
	# pos = np.arange(sorted_idx.shape[0]) + .5
	# pvals = feature_importance[sorted_idx]
	# pcols = X_train.columns[sorted_idx]
	# plt.figure(figsize=(8,12))
	# plt.barh(pos, pvals, align='center')
	# plt.yticks(pos, pcols)
	# plt.xlabel('Relative Importance')
	# plt.title('Variable Importance')
	# plt.show()
	# 
	# 

exit()