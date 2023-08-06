"""Utils for ML

"""

import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics.scorer import make_scorer
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from scipy import interp

from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import mutual_info_regression

from sklearn.feature_selection import f_classif
from sklearn.feature_selection import mutual_info_classif

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.cluster import KMeans

from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression 

import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import OneHotEncoder

from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout

from IPython.display import display, Markdown, HTML

import category_encoders

from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

__PRINT = 'PRINT'
__HTML = 'HTML'

__line_to_print = "________________________________________"

def print_separator():
	"""Prints a separator line using 80 underscores
	
    """
	
	print_new_line()
	display_func(__line_to_print + __line_to_print, mode=__PRINT)
	print_new_line()

def display_func(value_to_print, mode=None):
	"""Display or Print an object or string
		
	Args:
		value_to_print (Union[str, object]): Value to print
		mode (str): `PRINT` will use `print(value_to_print)`
			`HTML` will use `display(HTML(value_to_print))`
			default is `None` then use `display(value_to_print)`
			
    """
	
	if(mode == 'PRINT'):
		print(value_to_print)
	elif(mode == 'HTML'):
		display(HTML(value_to_print))
	else:
		display(value_to_print)

def print_new_line():
	"""Prints a new line
	
    """
	
	display_func("", mode=__PRINT)

def get_dataframe_from_array(data_array, columns):
	"""Convert ndarray to pd.DataFrame for the given list of columns
	
    Args:
		data_array (ndarray): Array to convert to pd.DataFrame
		columns (Union[array-like]): Column Names for the pd.DataFrame
	
    Returns:
		pd.DataFrame
		
    """
	
	df = pd.DataFrame(data_array, columns=columns)
	display_func("-> Loaded dataframe of shape " + str(df.shape))
	print_separator()
	return df

def about_dataframe(df):
	"""Describe DataFrame and show it's information
	
    Args:
		df (pd.DataFrame): DataFrame to describe and info
		
    """
	
	display_func("-> Data Describe\n", mode=__PRINT)
	display_func(df.describe(include = "all").transpose())
	print_separator()
	
	display_func("-> Data Info\n", mode=__PRINT)
	display_func(df.info())
	print_separator()
	
def null_values_info(df):
	"""Show null value information of a DataFrame
	
    Args:
		df (pd.DataFrame): DataFrame for which null values should be displayed
		
    """
	
	df = df.copy()
	kount_of_null_values = df.isnull().sum().sum()
	if(kount_of_null_values > 0):
		display_func("-> Null Values Info", mode=__PRINT)
		df_null_values_sum = df.isnull().sum()

		html_to_display = "<table><tbody><tr>"
		num_of_columns_with_null = 0
		for idx, each_feature in enumerate(sorted(df_null_values_sum.keys())):
			if(df_null_values_sum.loc[each_feature] > 0):
				html_to_display = (html_to_display + "<td>" + each_feature + 
					"</td>" + "<td>" +
					str(df_null_values_sum.loc[each_feature]) + 
					"</td>")
				num_of_columns_with_null = num_of_columns_with_null + 1
			if(num_of_columns_with_null%4 == 0):
				html_to_display = html_to_display + "</tr><tr>"
		html_to_display = html_to_display + "</tr></tbody></table>"
		display_func(html_to_display, __HTML)
	else:
		display_func("-> No Null Values", mode=__PRINT)
	
	print_separator()

def fill_null_values(df, column, value, row_index):
	"""Fill null values in a dataframe column
	
    Args:
		df (pd.DataFrame): DataFrame that will be updated
		column (str): Column in the target dataframe that will be updated
		value: (Union[int, str, object]): New value that will replace 
			null values
		row_index (Union[Index, array-like]): Index of rows to be updated
		
    """
	
	num_of_rows = row_index.shape[0]
	
	df.iloc[row_index, df.columns.get_loc(column)] = value
	display_func("{0:d} rows updated for '".format(num_of_rows) + column 
					+ "' with '" + str(value) + "'", mode=__PRINT)

def columns_info(df, cat_count_threshold, show_group_counts=False):
	"""Prints and returns column info for a given dataframe
	
    Args:
		df (pd.DataFrame): DataFrame
		cat_count_threshold (int): If a column in the dataframe 
			has unique value count less than this threshold then it 
			will be tagged as 'categorical'
		show_group_counts (boolean): If True then prints the individual 
			group counts for each column
	
	Example:
		`object_cat_cols, numeric_cat_cols, numeric_cols = utils.columns_info(
			data, cat_count_threshold=5, show_group_counts = True)`
	
    """
	
	if(cat_count_threshold is None):
		cat_count_threshold = 10
		
	all_columns = df.columns
	numeric_cat_columns = sorted(df._get_numeric_data().columns) 
	# https://stackoverflow.com/questions/29803093/
	# check-which-columns-in-dataframe-are-categorical
	object_cat_columns = sorted(list(set(all_columns) 
							- set(numeric_cat_columns)))
	
	display_func("-> Columns will be tagged as categorical if number " + 
					" of categories are less than or equal to " + 
					str(cat_count_threshold), mode=__PRINT)
	print_separator()
	
	kount = 0
	selected_object_cat_columns = []
	object_columns_not_identified_as_category = []
	to_print = "-> Count of 'object' type categorical columns {0:d}\n"
	to_print_detail = ""
	for object_column in object_cat_columns:
		if(df[object_column].unique().shape[0] <= cat_count_threshold):
			if(show_group_counts):
				to_print_detail = ( to_print_detail + 
					str(df.groupby(object_column)[object_column].count()) )
				to_print_detail = ( to_print_detail + 
					"\n" + 
					"\n________________________________________\n\n" )
			kount += 1
			selected_object_cat_columns.append(object_column)
		else:
			object_columns_not_identified_as_category.append(object_column)
		
	if(kount > 0):
		display_func(to_print.format(kount), mode=__PRINT)
		display_func(selected_object_cat_columns, mode=__PRINT)
		print_new_line()
		if(to_print_detail != ""):
			display_func(to_print_detail, mode=__PRINT)
		print_separator()
	
	if(len(object_columns_not_identified_as_category) > 0):
		display_func("-> Count of 'object' type non categorical columns: " + 
			str(len(object_columns_not_identified_as_category)) + 
			"\n", mode=__PRINT)
		display_func(object_columns_not_identified_as_category)
		print_new_line()
		print_separator()
		
	kount = 0
	selected_numeric_cat_columns = []
	numeric_columns = []
	to_print = "-> Count of 'numeric' type categorical columns {0:d}\n" 
	to_print_detail = ""
	for numeric_column in numeric_cat_columns:
		if(df[numeric_column].unique().shape[0] <= cat_count_threshold):
			if(show_group_counts):
				to_print_detail = to_print_detail + str(df.groupby(numeric_column)[numeric_column].count())
				to_print_detail = ( to_print_detail + "\n" + 
					"\n" + __line_to_print + "\n\n" )
			kount += 1
			selected_numeric_cat_columns.append(numeric_column)
		else:
			numeric_columns.append(numeric_column)
			
	if(kount > 0):
		display_func(to_print.format(kount), mode=__PRINT)
		display_func(selected_numeric_cat_columns, mode=__PRINT)
		print_new_line()
		if(to_print_detail != ""):
			display_func(to_print_detail, mode=__PRINT)
		print_separator()
	
	if(len(numeric_columns) > 0):
		display_func("Count of 'numeric' type columns: {0:d}\n".
			format(len(numeric_columns)), mode=__PRINT)
		display_func(numeric_columns, mode=__PRINT)
		print_new_line()
		print_separator()
	
	return (selected_object_cat_columns, 
		selected_numeric_cat_columns, 
		numeric_columns)

def get_X_and_y(df, y_column):
	"""Splits pd.dataframe into X (predictors) and y (response)
	
    Args:
		df (pd.DataFrame): DataFrame
		y_column (str): The response column name
	
    Returns:
		X (pd.DataFrame): All columns except the response will be in X
		y (pd.Series): Only the response column from dataframe
		
    """
	
	X = df[[i for i in list(df.columns) if i != y_column]]
	y = df[y_column]
	
	display_func("-> X set to " + ', '.join(
		df.columns[~df.columns.isin( [y_column] ) ] ) + "\n", mode=__PRINT)
	display_func("-> y set to " + y_column, mode=__PRINT)
	print_separator()
	
	return X, y

def __get_plot_attrs(**kwargs):
	if 'hue_column' not in kwargs:
		kwargs['hue_column'] = None
	
	if 'split_plots_by' not in kwargs:
		kwargs['split_plots_by'] = None
	
	if 'height' not in kwargs:
		kwargs['height'] = 4
	
	if 'aspect' not in kwargs:
		kwargs['aspect'] = 1
	
	if 'kde' not in kwargs:
		kwargs['kde']=True
		
	return ( kwargs['hue_column'], 
		kwargs['split_plots_by'], 
		kwargs['height'], 
		kwargs['aspect'],
		kwargs['kde'])

def count_plots(df, columns, **kwargs):
	"""Count Plots using seaborn
	
    Display Count plots for the given columns in a DataFrame
	
    Args:
        df (pd.DataFrame): DataFrame
        columns (array-like): Columns for which count plot has to be shown
		kwargs (dict of str): hue_column (for color)
			split_plots_by (to split seaborn facetgrid by column such as Gender)
			height (sets the height of plot)
			aspect (determines the widht of the plot based on height)
		
	Example:
		`utils.count_plots(data, object_cat_cols, height=4, aspect=1.5)`
		
    """
	
	(hue_column, 
	split_plots_by, 
	height, 
	aspect, 
	kde) = __get_plot_attrs(**kwargs)
	
	columns = pd.Series(columns)
	
	i = 0
	columns = columns[~columns.isin([hue_column, split_plots_by])]
	for each_col in columns:
		order=df.groupby(each_col)
		display_func("Count Plot for: " + str(each_col), mode=__PRINT)
		
		g = sns.catplot( x=each_col, hue=hue_column, 
			col=split_plots_by, kind="count", 
			data=df, order=order.indices.keys(), 
			height=height, aspect=aspect )
			
		g.set_xticklabels(rotation=40)
		plt.show()
		print_new_line()
		# display(HTML("<input type='checkbox' id='" + each_col + 
		# "' value='" + each_col + "'>" + each_col + "<br />"))
		i = i + 1

def count_compare_plots(df1, df1_title, df2, df2_title, column, **kwargs):
	"""Show Count Plots of two DataFrames for comparision
	
	Can be used to compare how Fill NA affects the distribution of a column

    Args:
        
	
	Example:
		The below example uses nhanes dataset.
		
		>>> for each_column in object_cat_columns:
				data[each_column] = data[each_column].fillna(
					data.groupby(['Gender'])[each_column].ffill())
		>>> for each_column in object_cat_columns:
		>>> 	str_count_of_nas = str(len(
					data_raw.index[data_raw.isnull()[each_column]]))
		>>> 	str_count_of_nas = ' (Count of NAs:' + str_count_of_nas + ')'
		>>> 	utils.count_compare_plots(df1=data_raw, 
				df1_title='Before Fill-NA' + str_count_of_nas, 
					df2=data, 
					df2_title='After Fill-NA', 
					column=each_column, 
					height=4, 
					aspect=1.5, 
					hue_column='Diabetes', 
					split_plots_by='Gender')
	
    """
	
	hue_column, split_plots_by, height, aspect = __get_plot_attrs(**kwargs)
	
	display_func("Count Plot for: " + str(column), mode=__PRINT)
	
	f, axes = plt.subplots(2)

	g = sns.catplot( x=column, hue=hue_column, col=split_plots_by, 
		kind="count", data=df1, height=height, aspect=aspect )
	g.set_xticklabels(rotation=40)
	g.fig.suptitle(df1_title, fontsize=16)
	
	###

	g = sns.catplot( x=column, hue=hue_column, col=split_plots_by, 
		kind="count", data=df2, height=height, aspect=aspect)
	g.set_xticklabels(rotation=40)
	g.fig.suptitle(df2_title, fontsize=16)
	
	####

	plt.close(1)
	plt.show()
	print_new_line()

def dist_plots(df, columns, **kwargs):
	"""Dist Plots using seaborn
	
    Args:
        df (pd.DataFrame): DataFrame
        columns (array-like): Columns for which count plot has to be shown
		kwargs (dict of str): hue_column (for color)
			split_plots_by (split seaborn FacetGrid by column, ex: Gender)
			height (sets the height of plot)
			aspect (determines the widht of the plot based on height)
	
	Example:
		`utils.dist_plots(data, numeric_cols, height=4, aspect=1.5, 
			hue_column='class', kde=False)`
		
    """
	
	kwargs['kde']=False
	
	kde_plots(df, columns, **kwargs)

def kde_plots(df, columns, **kwargs):
	"""KDE Plots using seaborn
	
    Args:
        df (pd.DataFrame): DataFrame
        columns (array-like): Columns for which count plot has to be shown
		kwargs (dict of str): hue_column (for color)
			split_plots_by (split seaborn FacetGrid by column, ex: Gender)
			height (sets the height of plot)
			aspect (determines the widht of the plot based on height)
	
	Example:
		`utils.kde_plots(data, numeric_cols, height=4, aspect=1.5, 
			hue_column='class')`
	
    """
	
	(hue_column, 
	split_plots_by, 
	height, 
	aspect, 
	kde) = __get_plot_attrs(**kwargs)
	
	columns = pd.Series(columns)
	
	for each_col in columns:
		if(kde):
			display_func("KDE Plot for: " + str(each_col), mode=__PRINT)
		else:
			display_func("Histogram for: " + str(each_col), mode=__PRINT)
		
		if(split_plots_by is None):
			if(hue_column is None):
				g = sns.FacetGrid(df[[each_col]], 
					height=height, 
					aspect=aspect)
			else:
				g = sns.FacetGrid(df[[each_col, hue_column]], 
					hue=hue_column, 
					height=height, 
					aspect=aspect)
		else:
			if(hue_column is None):
				g = sns.FacetGrid(df[[each_col, split_plots_by]], 
					col=split_plots_by, 
					height=height, 
					aspect=aspect)
			else:
				g = sns.FacetGrid(df[[each_col, hue_column, split_plots_by]], 
					hue=hue_column, 
					col=split_plots_by, 
					height=height,
					aspect=aspect)
					
		g = (g.map(sns.distplot, each_col, hist=True, kde=kde))
		g.add_legend()
		plt.show()
		print_new_line()

def kde_compare_plots(df1, df1_title, df2, df2_title, column, **kwargs):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	hue_column, split_plots_by, height, aspect = __get_plot_attrs(**kwargs)
	
	display_func("Count Plot for: " + str(column), mode=__PRINT)
	
	f, axes = plt.subplots(2)
	
	if(split_plots_by is None):
		g = sns.FacetGrid(df1[[column, hue_column]], hue=hue_column, 
			col=split_plots_by, height=height, 
			aspect=aspect)
	else:
		g = sns.FacetGrid(df1[[column, hue_column, split_plots_by]], 
			hue=hue_column, col=split_plots_by, height=height, 
				aspect=aspect)
	g = (g.map(sns.distplot, column, hist=True))
	g.add_legend()
	g.fig.suptitle(df1_title, fontsize=16)
	
	####
	
	if(split_plots_by is None):
		g = sns.FacetGrid(df2[[column, hue_column]], hue=hue_column, 
			col=split_plots_by, height=height, 
			aspect=aspect)
	else:
		g = sns.FacetGrid(df2[[column, hue_column, split_plots_by]], 
			hue=hue_column, col=split_plots_by, height=height, 
			aspect=aspect)
			
	g = (g.map(sns.distplot, column, hist=True))
	g.add_legend()
	g.fig.suptitle(df2_title, fontsize=16)
	
	plt.close(1)
	plt.show()
	print_new_line()
	
def encode_columns(df, method, columns = []):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	kount = 0
	df = df.copy()
		
	for columnName in columns:
		if(method == 'labelencoder'):
			label_encoder = LabelEncoder()
			df[columnName] = label_encoder.fit_transform(
				df[columnName].astype(str))
			display_func("-> Transformed [" + columnName + 
				"] using sklearn.LabelEncoder", mode=__PRINT)
			display_func("--> Classes: " + str(label_encoder.classes_), 
				mode=__PRINT)
		elif(method == 'binary'):
			label_binarizer = LabelBinarizer()
			lb_results = label_binarizer.fit_transform(df[columnName])
			display_func("-> Transformed [" + columnName + 
				"] using sklearn.LabelBinarizer")
			if(label_binarizer.y_type_ == 'multiclass'):
				display_func("--> Type of target data is: " + 
					label_binarizer.y_type_, mode=__PRINT)
				temp_df = pd.DataFrame(lb_results, 
					columns = label_binarizer.classes_, index = df.index)
				df = df.join(temp_df)
				display_func("--> Added following columns to dataframe: " + 
					str(label_binarizer.classes_), mode=__PRINT)
		elif(method == 'onehot'):
			one_hot_encoder = OneHotEncoder(sparse=False)
			ohe_results = one_hot_encoder.fit_transform(df[[columnName]])
			display_func("-> Transformed [" + columnName + 
				"] using sklearn.OneHotEncoder", mode=__PRINT)
			temp_df = pd.DataFrame(ohe_results, 
				columns = one_hot_encoder.get_feature_names())
			df = pd.concat([df,temp_df],axis=1)
			display_func("--> Added following columns to returned dataframe: " 
				+ str(one_hot_encoder.categories), mode=__PRINT)
		elif(method == 'pd_dummies'):
			df = pd.get_dummies(df, columns = columnName)
			display_func("-> Transformed [" + columnName + 
				"] using pd.get_dummies", mode=__PRINT)
		
		kount = kount + 1
		if(kount < len(columns)):
			display_func("", mode=__PRINT)
		
	print_separator()
	return df

def do_scaling(df, method, columns_to_scale=[]):
	"""Scale data using the specified method

    Columns specified in the arguments will be scaled

    Args:
        df (pd.DataFrame): DataFrame
		columns (array-like): List of columns that will be scaled
		
	Returns:
		df (pd.DataFrame)
	
    """
	
	if(method == 'StandardScaler'):
		scaler = StandardScaler()
		display_func("-> Data scaled using StandardScaler")
		print_separator()
		df_scaled = pd.DataFrame(scaler.fit_transform(df[columns_to_scale]), columns=columns_to_scale)
	
	df_not_scaled = df[ df.columns[ ~df.columns.isin( columns_to_scale ) ] ]
	df_scaled = df_scaled.join(df_not_scaled)
	
	return df_scaled
		
def do_feature_selection(X, y, method):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	if(method == 'f_regression'):
		skbest = SelectKBest(f_regression, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using skbest.f_regression", 
			mode=__PRINT)
		sf_data = {'Feature Name':selected_features.values, 
			'Score':skbest.scores_[mask]} 
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'mutual_info_regression'):
		skbest = SelectKBest(mutual_info_regression, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using " + 
			"skbest.mutual_info_regression", mode=__PRINT)
		sf_data = {'Feature Name':selected_features.values, 
			'Score':skbest.scores_[mask]}
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'RandomForestRegressor'):
		rf = RandomForestRegressor()
		
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
			random_state=42)
		rf.fit(X_train, y_train)
		
		cv_res = cross_validate(rf, X, y, cv=5, 
									scoring=('r2', 'neg_mean_squared_error'), 
									return_train_score=True,
									return_estimator =True)
									
		bst_tst_r2_idx = np.argmax(cv_res['test_r2'])
		bst_tst_estimator = cv_res['estimator'][bst_tst_r2_idx]

		feature_importances = pd.DataFrame(
			bst_tst_estimator.feature_importances_ ,
			index = X.columns,
			columns=['importance']).sort_values('importance', 
				ascending=False)
		display_func("-> Selected Features using Random Forest Regressor", 
			mode=__PRINT)
		display_func(feature_importances)
	elif(method == 'f_classif'):
		skbest = SelectKBest(f_classif, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using skbest.f_classif", 
			mode=__PRINT)
		sf_data = {'Feature Name':selected_features.values, 
			'Score':skbest.scores_[mask]} 
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'mutual_info_classif'):
		skbest = SelectKBest(mutual_info_classif, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using " + 
			"skbest.mutual_info_classif", mode=__PRINT)
		sf_data = {'Feature Name':selected_features.values, 
		'Score':skbest.scores_[mask]}
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'RandomForestClassifier'):
		rf = RandomForestClassifier()
		
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
			random_state=42)
		rf.fit(X_train, y_train)
		
		cv_res = cross_validate(rf, X, y, cv=5, 
									scoring=('r2', 'neg_mean_squared_error'), 
									return_train_score=True,
									return_estimator =True)
									
		bst_tst_r2_idx = np.argmax(cv_res['test_r2'])
		bst_tst_estimator = cv_res['estimator'][bst_tst_r2_idx]

		feature_importances = pd.DataFrame(
			bst_tst_estimator.feature_importances_ ,
			index = X.columns,
			columns=['importance']).sort_values('importance', 
				ascending=False)
		display_func("-> Selected Features using Random Forest Classifier", 
			mode=__PRINT)
		display_func(feature_importances,mode=__PRINT)
	
	print_separator()


def do_cross_validate(X, y, estimator_type, estimator, cv, **kwargs):
	"""Cross Validate (sklearn)
	
    Args:
	
	Example:
		cv_iterator = ShuffleSplit(n_splits=2, test_size=0.2, random_state=31)
		cv_results = utils.do_cross_validate(X_train, 
			y_train, 
			'Classification', 
			'DecisionTreeClassifier', 
			cv=cv_iterator, 
			kernel='rbf', 
			C=1, 
			gamma=0.01)
	
    """
	
	estimator_name = estimator
	if(estimator == 'LinearRegression'):
			estimator = LinearRegression()
	elif(estimator == 'LinearSVR'):
			estimator = LinearSVR()
	elif(estimator == 'SVR'):
			estimator = SVR()
	elif(estimator == 'LDA'):
			estimator = LinearDiscriminantAnalysis()
	elif(estimator == 'SVC'):
			estimator = SVC(kernel=kwargs['kernel'], 
				C=kwargs['C'], gamma=kwargs['gamma'])
	elif(estimator == 'DecisionTreeClassifier'):
			estimator = DecisionTreeClassifier()
	elif(estimator == 'RandomForestClassifier'):
			estimator = RandomForestClassifier(
				n_estimators=kwargs['n_estimators'], 
				max_features=kwargs['max_features'], 
				criterion=kwargs['criterion'])
	elif(estimator == 'GradientBoostingClassifier'):
			estimator = GradientBoostingClassifier( 
				n_estimators=int(kwargs['n_estimators']), 
				learning_rate=kwargs['learning_rate'], 
				max_depth=kwargs['max_depth'], 
				random_state=int(kwargs['random_state']) )
	elif(estimator == 'LogisticRegression'):
			estimator = LogisticRegression()
	else:
			estimator = None
	
	if(estimator is None):
		print("Estimator name not specified")
		print_separator()
		return
	
	if(estimator_type == 'Regression'):
		cv_res = cross_validate(estimator, 
			X, y, 
			cv=cv, 
			scoring=('r2', 'neg_mean_squared_error'), 
			return_train_score=True, 
			return_estimator=True)
		
		# train_r2		
		bst_trn_r2_idx = np.argmax(cv_res['train_r2'])
		bst_trn_r2 = cv_res['train_r2'][bst_trn_r2_idx]
		bst_trn_estimator = cv_res['estimator'][bst_trn_r2_idx]
		test_for_bst_trn_r2 = cv_res['test_r2'][bst_trn_r2_idx]
		fit_time_for_bst_trn_r2 = cv_res['fit_time'][bst_trn_r2_idx]
		score_time_for_bst_trn_r2 = cv_res['score_time'][bst_trn_r2_idx]
		mean_train_r2_score = np.mean(cv_res['train_r2'])
		
		# test_r2
		bst_tst_r2_idx = np.argmax(cv_res['test_r2'])
		bst_tst_r2 = cv_res['test_r2'][bst_tst_r2_idx]
		bst_tst_estimator = cv_res['estimator'][bst_tst_r2_idx]
		trn_for_bst_tst_r2 = cv_res['train_r2'][bst_tst_r2_idx]
		fit_time_for_bst_tst_r2 = cv_res['fit_time'][bst_tst_r2_idx]
		score_time_for_bst_tst_r2 = cv_res['score_time'][bst_tst_r2_idx]
		mean_test_r2_score = np.mean(cv_res['test_r2'])
		
		print("-> " + estimator_name + " scores\n");
		print("-> Mean Train R2 Score: %0.4f\n" %(mean_train_r2_score))
		print("-> Best Train R2 Score: %0.4f, " + 
			"Corresponding Test R2 Score: %0.4f, " + 
			"Best Train R2 Index: %d \n" 
			%(bst_trn_r2, test_for_bst_trn_r2, bst_trn_r2_idx))
		print("-> Mean Test R2 Score: %0.4f\n" %(mean_test_r2_score))
		print("-> Best Test R2 Score: {0:0.4f}, " + 
			"Corresponding Train R2 Score: {1:0.4f}, " + 
			"Best Test R2 Index: {2:d}".format(
				bst_tst_r2, trn_for_bst_tst_r2, bst_tst_r2_idx))
		
	elif (estimator_type == 'Classification'):
		scoring = {'accuracy': make_scorer(accuracy_score), 
				   'precision': make_scorer(precision_score, average='macro'), 
				   'recall': make_scorer(recall_score, average='macro'),
				   'roc': make_scorer(recall_score, average='macro')
				  }
		cv_res = cross_validate(estimator, 
			X, y, 
			cv=cv, 
			scoring=scoring, 
			return_train_score=True,
			return_estimator=True)
		
		# best trn_acc
		bst_trn_acc_index = np.argmax(cv_res['train_accuracy'])
		
		bst_trn_acc = cv_res['train_accuracy'][bst_trn_acc_index]
		tst_acc_for_bst_trn_acc = cv_res['test_accuracy'][bst_trn_acc_index]
		
		trn_prec_for_bst_trn_acc = cv_res['train_precision'][bst_trn_acc_index]
		tst_prec_for_bst_trn_acc = cv_res['test_precision'][bst_trn_acc_index]
		
		trn_rec_for_bst_trn_acc = cv_res['train_recall'][bst_trn_acc_index]
		tst_rec_for_bst_trn_acc = cv_res['test_recall'][bst_trn_acc_index]
		
		trn_roc_for_bst_trn_acc = cv_res['train_roc'][bst_trn_acc_index]
		tst_roc_for_bst_trn_acc = cv_res['test_roc'][bst_trn_acc_index]
		
		# best tst_acc
		bst_tst_acc_index = np.argmax(cv_res['test_accuracy'])
		
		bst_tst_acc = cv_res['test_accuracy'][bst_tst_acc_index]
		trn_acc_for_bst_tst_acc = cv_res['train_accuracy'][bst_tst_acc_index]
		
		trn_prec_for_bst_tst_acc = cv_res['train_precision'][bst_tst_acc_index]
		tst_prec_for_bst_tst_acc = cv_res['test_precision'][bst_tst_acc_index]
		
		trn_rec_for_bst_tst_acc = cv_res['train_recall'][bst_tst_acc_index]
		tst_rec_for_bst_tst_acc = cv_res['test_recall'][bst_tst_acc_index]
		
		trn_roc_for_bst_tst_acc = cv_res['train_roc'][bst_tst_acc_index]
		tst_roc_for_bst_tst_acc = cv_res['test_roc'][bst_tst_acc_index]
		
		
		# best trn_prec
		bst_trn_prec_index = np.argmax(cv_res['train_precision'])
		
		bst_trn_prec = cv_res['train_precision'][bst_trn_prec_index]
		tst_prec_for_bst_trn_prec = cv_res['test_precision'][bst_trn_prec_index]
		
		trn_acc_for_bst_trn_prec = cv_res['train_accuracy'][bst_trn_prec_index]
		tst_acc_for_bst_trn_prec = cv_res['test_precision'][bst_trn_prec_index]
		
		tst_rec_for_bst_trn_prec = cv_res['test_recall'][bst_trn_prec_index]
		trn_rec_for_bst_trn_prec = cv_res['train_recall'][bst_trn_prec_index]
		
		trn_roc_for_bst_trn_prec = cv_res['train_roc'][bst_trn_prec_index]
		tst_roc_for_bst_trn_prec = cv_res['test_roc'][bst_trn_prec_index]
		
		
		# best tst_prec
		bst_tst_prec_index = np.argmax(cv_res['test_precision'])
		
		bst_tst_prec = cv_res['test_precision'][bst_tst_prec_index]
		trn_prec_for_bst_tst_prec = cv_res['train_precision'][bst_tst_prec_index]
		
		trn_acc_for_bst_tst_prec = cv_res['train_accuracy'][bst_tst_prec_index]
		tst_acc_for_bst_tst_prec = cv_res['test_precision'][bst_tst_prec_index]
		
		tst_rec_for_bst_tst_prec = cv_res['test_recall'][bst_tst_prec_index]
		trn_rec_for_bst_tst_prec = cv_res['train_recall'][bst_tst_prec_index]
		
		trn_roc_for_bst_tst_prec = cv_res['train_roc'][bst_tst_prec_index]
		tst_roc_for_bst_tst_prec = cv_res['test_roc'][bst_tst_prec_index]
		
		
		# best trn_rec
		bst_trn_rec_index = np.argmax(cv_res['train_recall'])
		
		bst_trn_rec = cv_res['train_recall'][bst_trn_rec_index]
		tst_rec_for_bst_trn_rec = cv_res['test_recall'][bst_trn_rec_index]
		
		trn_prec_for_bst_trn_rec = cv_res['train_precision'][bst_trn_rec_index]
		tst_prec_for_bst_trn_rec = cv_res['test_precision'][bst_trn_rec_index]
		
		trn_acc_for_bst_trn_rec = cv_res['train_accuracy'][bst_trn_rec_index]
		tst_acc_for_bst_trn_rec = cv_res['test_precision'][bst_trn_rec_index]
		
		trn_roc_for_bst_trn_rec = cv_res['train_roc'][bst_trn_rec_index]
		tst_roc_for_bst_trn_rec = cv_res['test_roc'][bst_trn_rec_index]
		
		
		# best tst_rec
		bst_tst_rec_index = np.argmax(cv_res['test_recall'])
		
		bst_tst_rec = cv_res['test_recall'][bst_tst_rec_index]
		trn_rec_for_bst_tst_rec = cv_res['train_recall'][bst_tst_rec_index]
		
		trn_prec_for_bst_tst_rec = cv_res['train_precision'][bst_tst_rec_index]
		tst_prec_for_bst_tst_rec = cv_res['test_precision'][bst_tst_rec_index]
		
		trn_acc_for_bst_tst_rec = cv_res['train_accuracy'][bst_tst_rec_index]
		tst_acc_for_bst_tst_rec = cv_res['test_precision'][bst_tst_rec_index]
		
		trn_roc_for_bst_tst_rec = cv_res['train_roc'][bst_tst_rec_index]
		tst_roc_for_bst_tst_rec = cv_res['test_roc'][bst_tst_rec_index]
		
		
		# best trn_roc
		bst_trn_roc_index = np.argmax(cv_res['train_roc'])
		
		bst_trn_roc = cv_res['train_roc'][bst_trn_roc_index]
		tst_roc_for_bst_trn_roc = cv_res['test_roc'][bst_trn_roc_index]
		
		trn_rec_for_bst_trn_roc = cv_res['train_recall'][bst_trn_roc_index]
		tst_rec_for_bst_trn_roc = cv_res['test_recall'][bst_trn_roc_index]
		
		trn_prec_for_bst_trn_roc = cv_res['train_precision'][bst_trn_roc_index]
		tst_prec_for_bst_trn_roc = cv_res['test_precision'][bst_trn_roc_index]
		
		trn_acc_for_bst_trn_roc = cv_res['train_accuracy'][bst_trn_roc_index]
		tst_acc_for_bst_trn_roc = cv_res['test_precision'][bst_trn_roc_index]
		
		
		# best tst_roc
		bst_tst_roc_index = np.argmax(cv_res['test_roc'])
		
		bst_tst_roc = cv_res['test_roc'][bst_tst_roc_index]
		trn_roc_for_bst_tst_roc = cv_res['train_roc'][bst_tst_roc_index]
		
		trn_prec_for_bst_tst_roc = cv_res['train_precision'][bst_tst_roc_index]
		tst_prec_for_bst_tst_roc = cv_res['test_precision'][bst_tst_roc_index]
		
		trn_acc_for_bst_tst_roc = cv_res['train_accuracy'][bst_tst_roc_index]
		tst_acc_for_bst_tst_roc = cv_res['test_precision'][bst_tst_roc_index]
		
		trn_rec_for_bst_tst_roc = cv_res['train_recall'][bst_tst_roc_index]
		tst_rec_for_bst_tst_roc = cv_res['test_recall'][bst_tst_roc_index]
		
		
		indices = ['Train Accuracy', 'Test Accuracy', 
			'Train Precision', 'Test Precision', 'Train Recall', 
			'Test Recall', 'Train ROC', 'Test ROC']
		columns = ['Index', 'Best', 'Train Accuracy', 
			'Test Accuracy', 'Train Precision', 'Test Precision', 
			'Train Recall', 'Test Recall', 'Train ROC', 'Test ROC']
					
		d = [
			 [ bst_trn_acc_index, bst_trn_acc, 
				bst_trn_acc, tst_acc_for_bst_trn_acc, 
				trn_prec_for_bst_trn_acc, tst_prec_for_bst_trn_acc, 
				trn_rec_for_bst_trn_acc, tst_rec_for_bst_trn_acc, 
				trn_roc_for_bst_trn_acc, tst_roc_for_bst_trn_acc ],
			 
			 [ bst_tst_acc_index, bst_tst_acc, 
				trn_acc_for_bst_tst_acc, bst_tst_acc, 
				trn_prec_for_bst_tst_acc, tst_prec_for_bst_tst_acc, 
				trn_rec_for_bst_tst_acc, tst_rec_for_bst_tst_acc, 
				trn_roc_for_bst_tst_acc, tst_roc_for_bst_tst_acc ],
			 
			 [ bst_trn_prec_index, bst_trn_prec, 
				trn_acc_for_bst_trn_prec, tst_acc_for_bst_trn_prec, 
				bst_trn_prec, tst_prec_for_bst_trn_prec, 
				trn_rec_for_bst_trn_prec, tst_rec_for_bst_trn_prec, 
				trn_roc_for_bst_trn_prec, tst_roc_for_bst_trn_prec ],
			 
			 [ bst_tst_prec_index, bst_tst_prec, 
				trn_acc_for_bst_tst_prec, tst_acc_for_bst_tst_prec, 
				trn_prec_for_bst_tst_prec, bst_tst_prec, 
				trn_rec_for_bst_tst_prec, tst_rec_for_bst_tst_prec, 
				trn_roc_for_bst_tst_prec, tst_roc_for_bst_tst_prec ],
			 
			 [ bst_trn_rec_index, bst_trn_rec, 
				trn_acc_for_bst_trn_rec, tst_acc_for_bst_trn_rec, 
				trn_prec_for_bst_trn_rec, tst_prec_for_bst_trn_rec, 
				bst_trn_rec, tst_rec_for_bst_trn_rec, 
				trn_roc_for_bst_trn_rec, tst_roc_for_bst_trn_rec ],
			 
			 [ bst_tst_rec_index, bst_tst_rec, 
				trn_acc_for_bst_tst_rec, tst_acc_for_bst_tst_rec, 
				trn_prec_for_bst_tst_rec, tst_prec_for_bst_tst_rec, 
				trn_rec_for_bst_tst_rec, bst_tst_rec, 
				trn_roc_for_bst_tst_rec, tst_roc_for_bst_tst_rec ],
				
			 [ bst_trn_roc_index, bst_trn_roc, 
				trn_acc_for_bst_trn_roc, tst_acc_for_bst_trn_roc, 
				trn_prec_for_bst_trn_roc, tst_prec_for_bst_trn_roc, 
				trn_rec_for_bst_trn_roc, tst_rec_for_bst_trn_roc, 
				bst_trn_roc, tst_roc_for_bst_trn_roc ],
			 
			 [ bst_tst_roc_index, bst_tst_roc, 
				trn_acc_for_bst_tst_roc, tst_acc_for_bst_tst_roc, 
				trn_prec_for_bst_tst_roc, tst_prec_for_bst_tst_roc, 
				trn_rec_for_bst_tst_roc, tst_rec_for_bst_tst_roc, 
				trn_roc_for_bst_tst_roc, bst_tst_roc ],
			]
		
		df = pd.DataFrame(d, index = indices, columns = columns)
		
		display_func("-> " + estimator_name + " scores", mode=__PRINT) 
		display_func(df) # to format output similar to Jupyter's output
		
		# print(cv_res.keys())
	else:
		display_func("Estimator Type not specificed", mode=__PRINT)
		print_separator()
		return
	
	print_separator()
	# print(cv_res.keys())
	
	return cv_res

def print_confusion_matrix(y_true, y_pred):
	"""Prints the confision matrix with columns and index labels
	
    Args:
		y_true (Union[ndarray, pd.Series]): Actual Response
		y_pred (Union[ndarray, pd.Series]): Predicted Response
		
    """
	
	cfm_i = pd.DataFrame(confusion_matrix(y_true, y_pred))
	cfm_columns = []
	cfm_index = []
	# https://scikit-learn.org/stable/modules/generated/
	# sklearn.metrics.confusion_matrix.html
	#
	# List of labels to index the matrix. This may be used to reorder 
	# or select a subset of labels.
	# If none is given, those that appear at least once in y_true or 
	# y_pred are used in sorted order
	# 
	# As no labels are passed as args in the call to confusion_matrix 
	# then the classes are assigned on sorted order of unique values 
	# from response
	for each_class in sorted(np.unique(y_true)):
		cfm_columns.append("Predicted Class: " + str(each_class))
		cfm_index.append("Actual Class: " + str(each_class))
		
	cfm_i.columns = cfm_columns
	cfm_i.index = cfm_index
	display_func("-> Confusion Matrix", mode=__PRINT)
	display_func(cfm_i,mode=None)

def plot_decision_boundary(x_axis_data, y_axis_data, response, estimator):
	"""Plots the decision boundary

    

    Args:
        
		
    """
	
	plt.figure(figsize=(12,6))
	plt.scatter( x_axis_data, y_axis_data, c=response, cmap=plt.cm.Paired )
	h = .02  # step size in the mesh
	# create a mesh to plot in
	x_min, x_max = x_axis_data.min() - 1, x_axis_data.max() + 1
	y_min, y_max = y_axis_data.min() - 1, y_axis_data.max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), 
		np.arange(y_min, y_max, h))

	# Plot the decision boundary. For that, we will assign a color to each
	# point in the mesh [x_min, m_max]x[y_min, y_max].
	Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.contour(xx, yy, Z, cmap=plt.cm.Paired)

# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
# def plot_roc_curve(estimator, X_train, X_test, y_train, y_test, classes, is_for_outlier_detection=False):
	# """Summary line.

    # Extended description of function.

    # Args:
        
		
    # """
	
	# num_of_classes = len(classes)
	# if(num_of_classes < 2):
		# print("Number of classes have to be greater than or equal to 2")
		# return None
	
	# # typical classes are 0,1 or -1, 1 in two class responses. 
	# # if not then will this work?
	# if(num_of_classes == 2):
		# classifier = OneVsRestClassifier(estimator)
		# if(is_for_outlier_detection):
			# y_pred = estimator.fit(X_train).predict(X_test)
		# else:
			# y_pred = classifier.fit(X_train, y_train).predict(X_test)
		# fpr, tpr, thresholds = roc_curve(y_test, y_pred)
		# roc_auc = roc_auc_score(y_test, y_pred)
		# lw = 2
		# plt.figure(figsize=(12,6))
		# plt.plot(fpr, tpr, lw=2)
		
		# # random predictions curve
		# plt.plot([0, 1], [0, 1], linestyle='--', lw=lw)
		
		# plt.xlim([-0.001, 1.0])
		# plt.ylim([0.0, 1.05])
		# plt.xlabel('False Positive Rate')
		# plt.ylabel('True Positive Rate')
		# plt.title('Receiver Operating Characteristic (area = %0.3f)' %roc_auc)
		# return fpr, tpr, roc_auc

	# # when number of classes is more than 2 then
	
	# # Binarize the output
	
	# # converts 3 classes in one column to 3 columns binary matrix
	# y_test = label_binarize(y_test, classes=classes)
	
	# num_of_classes = y_test.shape[1]

	# # Learn to predict each class against the other
	# classifier = OneVsRestClassifier(estimator)
	
	# # as of now found that SVM only has the decision_function implemented
	# if hasattr(classifier, "decision_function"):
		# y_pred = classifier.fit(X_train, y_train).decision_function(X_test)
	# else:
		# y_pred = classifier.fit(X_train, y_train).predict_proba(X_test)
	
	# # Compute ROC curve and ROC area for each class
	# fpr = dict()
	# tpr = dict()
	# roc_auc = dict()
	# for i in range(num_of_classes):
		# fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
		# roc_auc[i] = auc(fpr[i], tpr[i])

	# # Compute micro-average ROC curve and ROC area
	# fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_pred.ravel())
	# roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	
	# plot_roc_curve_multiclass(fpr, tpr, roc_auc, classes)
	
	# return fpr, tpr, roc_auc

def plot_roc_curve_binary_class(y_true, y_pred):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	num_of_classes = len(np.unique(y_true))
	if(num_of_classes != 2):
		print("Number of classes should be equal to 2")
		return None
	
	fpr, tpr, thresholds = roc_curve(y_true, y_pred)
	roc_auc = roc_auc_score(y_true, y_pred)
	lw = 2
	plt.figure(figsize=(12,6))
	plt.plot(fpr, tpr, lw=2)
	
	# random predictions curve
	plt.plot([0, 1], [0, 1], linestyle='--', lw=lw)
	
	plt.xlim([-0.001, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver Operating Characteristic (area = %0.3f)' %roc_auc)
	
	return fpr, tpr, roc_auc

# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
def plot_roc_curve_multiclass(estimator, X_train, X_test, y_train, y_test):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	# converts 3 classes in one column to 3 columns binary matrix
	y_test = label_binarize(y_test, classes=classes)
	
	# get the total number of classes in y_test
	num_of_classes = y_test.shape[1]
	
	# Learn to predict each class against the other
	classifier = OneVsRestClassifier(estimator)
	
	# as of now found that SVM only has the decision_function implemented
	if hasattr(classifier, "decision_function"):
		y_test_pred = classifier.fit(X_train, 
									y_train).decision_function(X_test)
	else:
		y_test_pred = classifier.fit(X_train, y_train).predict_proba(X_test)
	
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	for i in range(num_of_classes):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_test_pred[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

	# Compute micro-average ROC curve and ROC area
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_test_pred.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	
	# First aggregate all false positive rates
	all_fpr = np.unique(
		np.concatenate([fpr[i] for i in range(num_of_classes)]) )

	# Then interpolate all ROC curves at this points
	mean_tpr = np.zeros_like(all_fpr)
	for i in range(num_of_classes):
		mean_tpr += interp(all_fpr, fpr[i], tpr[i])

	# Finally average it and compute AUC
	mean_tpr /= num_of_classes

	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

	# Plot all ROC curves
	# plt.figure()
	plt.figure(figsize=(12,6))
	plt.plot(fpr["micro"], tpr["micro"],
			 label='micro-average ROC curve (area = {0:0.2f})'
				   ''.format(roc_auc["micro"]),
			 color='deeppink', linestyle=':', linewidth=4)

	plt.plot(fpr["macro"], tpr["macro"],
			 label='macro-average ROC curve (area = {0:0.2f})'
				   ''.format(roc_auc["macro"]),
			 color='navy', linestyle=':', linewidth=4)

	colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
	lw = 2
	
	for i, color in zip(range(num_of_classes), colors):
		plt.plot(fpr[i], tpr[i], color=color, lw=lw,
				 label='ROC curve of class {0} (area = {1:0.2f})'
				 ''.format(classes[i], roc_auc[i]))
	
	plt.plot([0, 1], [0, 1], 'k--', lw=lw)
	plt.xlim([-0.001, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Extension of ROC to multi-class')
	plt.legend(loc="lower right")
	plt.show()

def do_outlier_detection(df, target_column, outlier_classes, 
						method, **kwargs):
	
	predictor_columns = df.columns[~df.columns.isin([target_column])]
	
	# copy of dataframe
	df = df.copy()
	
	# convert target column to str type
	df[target_column] = df[target_column].astype('str')
	
	# assign all values that are outliers as -1
	for outlier_class in outlier_classes:
		df.loc[(df[target_column] == str(outlier_class)), target_column] = -1
	
	# assign the rest as inliers
	df.loc[~(df[target_column] == -1), target_column] = 1
	
	if(method == 'OneClassSVM'):
		display_func("Using " + method +" for Outlier Detection", __PRINT)
		print_new_line()
		inliers = df[df[target_column] == 1]
		outliers = df[~(df[target_column] == 1)]

		del inliers[target_column]
		del outliers[target_column]
		
		classifier = svm.OneClassSVM(kernel=kwargs['kernel'], nu=kwargs['nu'], 
									gamma='scale')
		classifier.fit(inliers)

		inlier_pred = classifier.predict(inliers)
		error_inlier_pred = inlier_pred[inlier_pred == -1].size
		pct_error_inlier_pred = (error_inlier_pred/inliers.shape[0]) * 100
		display_func("Error Inlier Pred (inliers classified as outliers):" + 
			str(error_inlier_pred) + ", Percentage Error: " + 
			str( round(pct_error_inlier_pred,2) ), mode=__PRINT)

		outlier_pred = classifier.predict(outliers)
		error_outlier_pred = outlier_pred[outlier_pred == 1].size
		pct_error_outlier_pred = (error_outlier_pred/outliers.shape[0]) * 100
		display_func("Error Outlier Pred (outliers classified as inliers):" + 
						str(error_outlier_pred) + ", Percentage Error: " + 
						str( round(pct_error_outlier_pred,2) ), mode=__PRINT)
		
		print_new_line()
		
		y_true = df[target_column]
		y_pred = classifier.predict(df[predictor_columns])
		
		display_func("Confusion Matrix after Predict on Entire Data", 
						mode=__PRINT)
		print_confusion_matrix(y_true, y_pred)
		print_new_line()
		
		display_func("Classification Report after Predict on Entire Data", 
						mode=__PRINT)
		print(classification_report(y_true, y_pred))
		
		if(len(predictor_columns) == 2):
			display_func("Plotting Boundary", mode=__PRINT)
			plot_decision_boundary(df[predictor_columns[0]], 
								df[predictor_columns[1]], 
								df[target_column], classifier)
		return classifier
	elif(method=='IsolationForest'):
		display_func("Using " + method +" for Outlier Detection", __PRINT)
		print_new_line()
		X, y = get_X_and_y(df, target_column)
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
															random_state=42)
		classifier = IsolationForest(behaviour='new', 
									random_state=42, 
									contamination=kwargs['contamination'])
		classifier.fit(X_train)
		y_test_pred = classifier.predict(X_test)
		
		display_func("Confusion Matrix after Predict on Test Data", 
						mode=__PRINT)
		print_confusion_matrix(y_test, y_test_pred)
		print_new_line()
		
		display_func("Classification Report after Predict on Test Data", 
						mode=__PRINT)
		print(classification_report(y_test, y_test_pred))
		
		if(len(predictor_columns) == 2):
			display_func("Plotting Boundary", mode=__PRINT)
			plot_decision_boundary(X_test[predictor_columns[0]], 
								X_test[predictor_columns[1]], 
								y_test, classifier)
		return classifier
	elif(method=='LocalOutlierFactor'):
		display_func("Using " + method +" for Outlier Detection", __PRINT)
		print_new_line()
		X, y = get_X_and_y(df, target_column)
		classifier = LocalOutlierFactor(n_neighbors=kwargs['n_neighbors'])
		y_pred = classifier.fit_predict(X)
		
		display_func("Confusion Matrix after Predict on Test Data", 
						mode=__PRINT)
		print_confusion_matrix(y, y_pred)
		print_new_line()
		
		display_func("Classification Report after Predict on Test Data", 
						mode=__PRINT)
		print(classification_report(y, y_pred))
		
		return classifier