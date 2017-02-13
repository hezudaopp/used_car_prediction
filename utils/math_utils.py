# -*- coding: UTF-8 -*-
import re
import numpy as np
import scipy as sp
import scipy.stats

"""parse percentage string to float"""
def percentage_to_float(percentage_str):
	if percentage_str is None:
		return 0.0
	return float(re.search(r'[\d\.]+', percentage_str).group()) * 0.01

"""compute data's mean confidence interval,
mean difference will also be returned."""
def mean_confidence_interval(data, confidence=0.95):
	a = 1.0 * np.array(data)
	n = len(a)
	if n < 1: return -1, -1, -1
	m, se = np.mean(a), scipy.stats.sem(a)
	h = se * sp.stats.t._ppf((1 + confidence) / 2.0, n-1)
	return m, m-h, m+h

"""self defined loss function"""
def mean_loss_percentage(ground_truth, predictions):
	return np.mean(np.abs((ground_truth - predictions) / predictions))