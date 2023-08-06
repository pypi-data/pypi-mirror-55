import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Analysis -----------------------------------------------------------------------------

def separateFeatures(data):
	"""
	Separates feature by type (First Order, Shape, GLCM...).

	Parameters
	----------
	data : pandas.DataFrame
		Data with features calculated.

	Returns
	-------
	columns_dict : dict
		Dict with keys as feature's type.

	Examples
	--------

	>>> c_dict = separateFeatures(data)
	>>> c_dict['GLCM']
	  Autocorrelation_GLCM ClusterProminence_GLCM  ...      SumEntropy_GLCM    SumSquares_GLCM
	0   19.291666666666668    0.01707175925925927  ...  0.23978697925681078  5.822048611111111

	"""
	list_type = list(map(lambda s: s.split('_')[-1], data.columns[1:]))
	set_type = list(set(list_type))

	columns_dict = {}
	for feat_type in set_type:
		columns_dict[feat_type] = data[data.columns[1:][pd.Index(list_type).isin([feat_type])]]

	return columns_dict
