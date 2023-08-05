"""Utils for ML

This module wraps boilerplate code used to perform routine ML related tasks

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

__PRINT = 'PRINT'
__HTML = 'HTML'

def print_separator():
	"""Prints a separator line using 80 underscores
	
    """
	
	print_new_line
	display_func("________________________________________________________________________________", mode=__PRINT)
	print_new_line()

def display_func(value_to_print, mode=None):
	"""Display or Print an object or string based on `mode` using `IPython.display` or using `print`
	
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

def get_data_from_array(data_array, columns):
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
		df (pd.DataFrame): DataFrame on which describe and info is to be called
		
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
				html_to_display = html_to_display + "<td>" + each_feature + "</td>" + "<td>" + str(df_null_values_sum.loc[each_feature]) + "</td>"
				num_of_columns_with_null = num_of_columns_with_null + 1
			if(num_of_columns_with_null%4 == 0):
				html_to_display = html_to_display + "</tr><tr>"
		html_to_display = html_to_display + "</tr></tbody></table>"
		display_func(html_to_display, __HTML)
	else:
		display_func("-> No Null Values", mode=__PRINT)
	
	print_separator()

def fill_null_values(df, column, value, row_index):
	"""Fill null values in a dataframe column. Prints out number of rows updated with the new value.
	
    Args:
		df (pd.DataFrame): DataFrame that will be updated
		column (str): Column in the target dataframe that will be updated
		value: (Union[int, str, object]): New value that will replace null values
		row_index (Union[Index, array-like]): Index of rows that should be updated
		
    """
	
	num_of_rows = row_index.shape[0]
	
	df.iloc[row_index, df.columns.get_loc(column)] = value
	display_func("{0:d} rows updated for '".format(num_of_rows) + column + "' with '" + str(value) + "'", mode=__PRINT)

def columns_info(df, cat_count_threshold, show_group_counts=False):
	"""Prints and returns column info for a given dataframe
	
    Args:
		df (pd.DataFrame): DataFrame
		cat_count_threshold (int): If a column in the dataframe has unique value count less than this threshold then it will be assumed 'categorical'
		show_group_counts (boolean): If True then prints the individual group counts for each column
		
    """
	
	if(cat_count_threshold is None):
		cat_count_threshold = 10
		
	all_columns = df.columns
	numeric_cat_columns = sorted(df._get_numeric_data().columns) ## https://stackoverflow.com/questions/29803093/check-which-columns-in-dataframe-are-categorical
	object_cat_columns = sorted(list(set(all_columns) - set(numeric_cat_columns)))
	
	display_func("-> Columns will be tagged as categorical if number of categories are less than or equal to " + str(cat_count_threshold), mode=__PRINT)
	print_separator()
	
	kount = 0
	selected_object_cat_columns = []
	object_columns_not_identified_as_category = []
	to_print = "-> Count of 'object' type categorical columns {0:d}\n"
	to_print_detail = ""
	for object_column in object_cat_columns:
		if(df[object_column].unique().shape[0] <= cat_count_threshold):
			if(show_group_counts):
				to_print_detail = to_print_detail + str(df.groupby(object_column)[object_column].count())
				to_print_detail = to_print_detail + "\n" + "\n________________________________________\n\n"
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
		display_func("-> Count of 'object' type non categorical columns: " + str(len(object_columns_not_identified_as_category)) + "\n", mode=__PRINT)
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
				to_print_detail = to_print_detail + "\n" + "\n________________________________________\n\n"
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
		display_func("Count of 'numeric' type columns: {0:d}\n".format(len(numeric_columns)), mode=__PRINT)
		display_func(numeric_columns, mode=__PRINT)
		print_new_line()
		print_separator()
	
	return selected_object_cat_columns, selected_numeric_cat_columns, numeric_columns

def get_X_and_y(df, y_column):
	"""Splits and returns dataframe as a tuple of X (predictors) and y (response)
	
    Args:
		df (pd.DataFrame): DataFrame
		y_column (str): The response column name
	
    Returns:
		X (pd.DataFrame): All columns except the response will be in X
		y (pd.Series): Only the response column from dataframe
		
    """
	
	X = df[[i for i in list(df.columns) if i != y_column]]
	y = df[y_column]
	
	display_func("-> X set to " + ', '.join(df.columns[~df.columns.isin( [y_column] ) ] ) + "\n", mode=__PRINT)
	display_func("-> y set to " + y_column, mode=__PRINT)
	print_separator()
	
	return X, y
	
def count_plots(df, columns, args, hue_column=None, split_plots_by=None):
	"""Count plots using Seaborn

    Display Count plots for the given columns in a DataFrame

    Args:
        df (pd.DataFrame): DataFrame
        columns (array-like): Columns for which count plot has to be shown
		args (pd.Series): Description of arg2
		hue_column (str, optional): Category Column for `hue`
		split_plots_by (str, optional): Category Column to split the count plots, example: Gender
		
    """
	
	i = 0
	columns = columns[~columns.isin([hue_column, split_plots_by])]
	for each_col in columns:
		order=df.groupby(each_col)
		display_func("Count Plot for: " + str(each_col), mode=__PRINT)
		g = sns.catplot( x=each_col, hue=hue_column, col=split_plots_by, kind="count", data=df, order=order.indices.keys(), height=args.loc['height'], aspect=args.loc['aspect'] )
		g.set_xticklabels(rotation=40)
		plt.show()
		print_new_line()
		# display(HTML("<input type='checkbox' id='" + each_col + "' value='" + each_col + "'>" + each_col + "<br />"))
		i = i + 1

def count_compare_plots(df1, df1_title, df2, df2_title, column, args, hue_column=None, split_plots_by=None):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	display_func("Count Plot for: " + str(column), mode=__PRINT)
	
	f, axes = plt.subplots(2)

	g = sns.catplot( x=column, hue=hue_column, col=split_plots_by, kind="count", data=df1, height=args.loc['height'], aspect=args.loc['aspect'])
	g.set_xticklabels(rotation=40)
	g.fig.suptitle(df1_title, fontsize=16)
	
	###

	g = sns.catplot( x=column, hue=hue_column, col=split_plots_by, kind="count", data=df2, height=args.loc['height'], aspect=args.loc['aspect'])
	g.set_xticklabels(rotation=40)
	g.fig.suptitle(df2_title, fontsize=16)
	
	####

	plt.close(1)
	plt.show()
	print_new_line()

def kde_plots(df, columns, args, hue_column=None, split_plots_by=None):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	for each_col in columns:
		display_func("KDE Plot for: " + str(each_col), mode=__PRINT)
		if(split_plots_by is None):
			if(hue_column is None):
				g = sns.FacetGrid(df[[each_col]], height=args.loc['height'], aspect=args.loc['aspect'])
			else:
				g = sns.FacetGrid(df[[each_col, hue_column]], hue=hue_column, height=args.loc['height'], aspect=args.loc['aspect'])
		else:
			if(hue_column is None):
				g = sns.FacetGrid(df[[each_col, split_plots_by]], col=split_plots_by, height=args.loc['height'], aspect=args.loc['aspect'])
			else:
				g = sns.FacetGrid(df[[each_col, hue_column, split_plots_by]], hue=hue_column, col=split_plots_by, height=args.loc['height'], aspect=args.loc['aspect'])
		g = (g.map(sns.distplot, each_col, hist=True))
		g.add_legend()
		plt.show()
		print_new_line()

def kde_compare_plots(df1, df1_title, df2, df2_title, column, args, hue_column=None, split_plots_by=None):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	display_func("Count Plot for: " + str(column), mode=__PRINT)
	
	f, axes = plt.subplots(2)
	
	if(split_plots_by is None):
		g = sns.FacetGrid(df1[[column, hue_column]], hue=hue_column, col=split_plots_by, height=args.loc['height'], aspect=args.loc['aspect'])
	else:
		g = sns.FacetGrid(df1[[column, hue_column, split_plots_by]], hue=hue_column, col=split_plots_by, height=args.loc['height'], aspect=args.loc['aspect'])
	g = (g.map(sns.distplot, column, hist=True))
	g.add_legend()
	g.fig.suptitle(df1_title, fontsize=16)
	
	####
	
	if(split_plots_by is None):
		g = sns.FacetGrid(df2[[column, hue_column]], hue=hue_column, col=split_plots_by, height=args.loc['height'], aspect=args.loc['aspect'])
	else:
		g = sns.FacetGrid(df2[[column, hue_column, split_plots_by]], hue=hue_column, col=split_plots_by, height=args.loc['height'], aspect=args.loc['aspect'])
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
	encoder_to_return = None
	df = df.copy()
	
	if(method == 'labelencoder'):
		label_encoder = LabelEncoder()
		encoder_to_return = label_encoder
	elif(method == 'binary'):
		label_binarizer = LabelBinarizer()
		encoder_to_return = label_binarizer
	elif(method == 'onehot'):
		one_hot_encoder = OneHotEncoder(sparse=False)
		encoder_to_return = one_hot_encoder
	elif(method == 'pd_dummies'):
		encoder_to_return = None
		
	for columnName in columns:
		if(method == 'labelencoder'):
			df[columnName] = label_encoder.fit_transform(df[columnName].astype(str))
			display_func("-> Transformed X[" + columnName + "] using sklearn.LabelEncoder") 
		elif(method == 'binary'):
			lb_results = label_binarizer.fit_transform(df[columnName])
			display_func("-> Transformed X[" + columnName + "] using sklearn.LabelBinarizer")
			if(label_binarizer.y_type_ == 'multiclass'):
				display_func("--> Type of target data is: " + label_binarizer.y_type_)
				temp_df = pd.DataFrame(lb_results, columns = label_binarizer.classes_, index = df.index)
				df = df.join(temp_df)
				display_func("--> Added following columns to dataframe: " + str(label_binarizer.classes_))
		elif(method == 'onehot'):
			ohe_results = one_hot_encoder.fit_transform(df[[columnName]])
			display_func("-> Transformed X[" + columnName + "] using sklearn.OneHotEncoder.")
			temp_df = pd.DataFrame(ohe_results, columns = one_hot_encoder.get_feature_names())
			df = pd.concat([df,temp_df],axis=1)
			display_func("--> Added following columns to returned dataframe: " + str(one_hot_encoder.categories))
		elif(method == 'pd_dummies'):
			df = pd.get_dummies(df, columns = columnName)
			display_func("-> Transformed X[" + columnName + "] using pd.get_dummies.")
		
		kount = kount + 1
		if(kount < len(columns)):
			display_func("")
		
	print_separator()
	return df, encoder_to_return

def do_scaling(df, method):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	if(method == 'StandardScaler'):
		scaler = StandardScaler()
		display_func("-> Data scaled using StandardScaler")
		print_separator()
		columns = df.columns
		return pd.DataFrame(scaler.fit_transform(df), columns=columns)
		
		
def do_feature_selection(X, y, method):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	if(method == 'f_regression'):
		skbest = SelectKBest(f_regression, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using skbest.f_regression")
		sf_data = {'Feature Name':selected_features.values, 'Score':skbest.scores_[mask]} 
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'mutual_info_regression'):
		skbest = SelectKBest(mutual_info_regression, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using skbest.mutual_info_regression")
		sf_data = {'Feature Name':selected_features.values, 'Score':skbest.scores_[mask]}
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'RandomForestRegressor'):
		rf = RandomForestRegressor()
		
		X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
		rf.fit(X_train, y_train)
		
		cv_results = cross_validate(rf, X, y, cv=5, 
									scoring=('r2', 'neg_mean_squared_error'), 
									return_train_score=True,
									return_estimator =True)
									
		best_test_r2_score_index = np.argmax(cv_results['test_r2'])
		best_test_estimator = cv_results['estimator'][best_test_r2_score_index]

		feature_importances = pd.DataFrame(best_test_estimator.feature_importances_ ,
										   index = X.columns,
										   columns=['importance']).sort_values('importance', ascending=False)
		display_func("-> Selected Features using Random Forest Regressor")
		display_func(feature_importances)
	elif(method == 'f_classif'):
		skbest = SelectKBest(f_classif, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using skbest.f_classif")
		sf_data = {'Feature Name':selected_features.values, 'Score':skbest.scores_[mask]} 
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'mutual_info_classif'):
		skbest = SelectKBest(mutual_info_classif, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		display_func("-> Selected Features using skbest.mutual_info_classif")
		sf_data = {'Feature Name':selected_features.values, 'Score':skbest.scores_[mask]}
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		display_func(sf_df)
	elif(method == 'RandomForestClassifier'):
		rf = RandomForestClassifier()
		
		X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
		rf.fit(X_train, y_train)
		
		cv_results = cross_validate(rf, X, y, cv=5, 
									scoring=('r2', 'neg_mean_squared_error'), 
									return_train_score=True,
									return_estimator =True)
									
		best_test_r2_score_index = np.argmax(cv_results['test_r2'])
		best_test_estimator = cv_results['estimator'][best_test_r2_score_index]

		feature_importances = pd.DataFrame(best_test_estimator.feature_importances_ ,
										   index = X.columns,
										   columns=['importance']).sort_values('importance', ascending=False)
		display_func("-> Selected Features using Random Forest Classifier")
		display_func(feature_importances,mode=__PRINT)
	
	print_separator()


def do_cross_validate(X, y, estimator_type, estimator, cv, args):
	"""Summary line.

    Extended description of function.

    Args:
        
		
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
			estimator = SVC(kernel=args.loc['kernel'], C=args.loc['C'], gamma=args.loc['gamma'])
	elif(estimator == 'DecisionTreeClassifier'):
			estimator = DecisionTreeClassifier()
	elif(estimator == 'RandomForestClassifier'):
			estimator = RandomForestClassifier(n_estimators=args.loc['n_estimators'], max_features=args.loc['max_features'], criterion=args.loc['criterion'])
	elif(estimator == 'GradientBoostingClassifier'):
			estimator = GradientBoostingClassifier( n_estimators=int(args.loc['n_estimators']), 
													learning_rate=args.loc['learning_rate'], 
													max_depth=args.loc['max_depth'], 
													random_state=int(args.loc['random_state']) )
	elif(estimator == 'LogisticRegression'):
			estimator = LogisticRegression()
	else:
			estimator = None
	
	if(estimator is None):
		print("Estimator name not specified")
		print_separator()
		return
	
	if(estimator_type == 'Regression'):
		cv_results = cross_validate(estimator, X, y, cv=cv, 
									scoring=('r2', 'neg_mean_squared_error'), 
									return_train_score=True,
									return_estimator =True)
		
		# train_r2		
		best_train_r2_score_index = np.argmax(cv_results['train_r2'])
		best_train_r2_score = cv_results['train_r2'][best_train_r2_score_index]
		best_train_estimator = cv_results['estimator'][best_train_r2_score_index]
		test_for_best_train_r2_score = cv_results['test_r2'][best_train_r2_score_index]
		fit_time_for_best_train_r2_score = cv_results['fit_time'][best_train_r2_score_index]
		score_time_for_best_train_r2_score = cv_results['score_time'][best_train_r2_score_index]
		mean_train_r2_score = np.mean(cv_results['train_r2'])
		
		# test_r2
		best_test_r2_score_index = np.argmax(cv_results['test_r2'])
		best_test_r2_score = cv_results['test_r2'][best_test_r2_score_index]
		best_test_estimator = cv_results['estimator'][best_test_r2_score_index]
		train_for_best_test_r2_score = cv_results['train_r2'][best_test_r2_score_index]
		fit_time_for_best_test_r2_score = cv_results['fit_time'][best_test_r2_score_index]
		score_time_for_best_test_r2_score = cv_results['score_time'][best_test_r2_score_index]
		mean_test_r2_score = np.mean(cv_results['test_r2'])
		
		print("-> " + estimator_name + " scores\n");
		print("-> Mean Train R2 Score: %0.4f\n" %(mean_train_r2_score))
		print("-> Best Train R2 Score: %0.4f, Corresponding Test R2 Score: %0.4f, Best Train R2 Index: %d \n" %(best_train_r2_score, test_for_best_train_r2_score, best_train_r2_score_index))
		print("-> Mean Test R2 Score: %0.4f\n" %(mean_test_r2_score))
		print("-> Best Test R2 Score: {0:0.4f}, Corresponding Train R2 Score: {1:0.4f}, Best Test R2 Index: {2:d}".format(best_test_r2_score, train_for_best_test_r2_score, best_test_r2_score_index))
		
	elif (estimator_type == 'Classification'):
		scoring = {'accuracy': make_scorer(accuracy_score), 
				   'precision': make_scorer(precision_score, average='macro'), 
				   'recall': make_scorer(recall_score, average='macro'),
				   'roc': make_scorer(recall_score, average='macro')
				  }
		cv_results = cross_validate(estimator, X, y, cv=cv, 
									scoring=scoring, 
									return_train_score=True,
									return_estimator =True)
		
		# best train_accuracy
		best_train_accuracy_index = np.argmax(cv_results['train_accuracy'])
		
		best_train_accuracy = cv_results['train_accuracy'][best_train_accuracy_index]
		test_accuracy_for_best_train_accuracy = cv_results['test_accuracy'][best_train_accuracy_index]
		
		train_precision_for_best_train_accuracy = cv_results['train_precision'][best_train_accuracy_index]
		test_precision_for_best_train_accuracy = cv_results['test_precision'][best_train_accuracy_index]
		
		train_recall_for_best_train_accuracy = cv_results['train_recall'][best_train_accuracy_index]
		test_recall_for_best_train_accuracy = cv_results['test_recall'][best_train_accuracy_index]
		
		train_roc_for_best_train_accuracy = cv_results['train_roc'][best_train_accuracy_index]
		test_roc_for_best_train_accuracy = cv_results['test_roc'][best_train_accuracy_index]
		
		# best test_accuracy
		best_test_accuracy_index = np.argmax(cv_results['test_accuracy'])
		
		best_test_accuracy = cv_results['test_accuracy'][best_test_accuracy_index]
		train_accuracy_for_best_test_accuracy = cv_results['train_accuracy'][best_test_accuracy_index]
		
		train_precision_for_best_test_accuracy = cv_results['train_precision'][best_test_accuracy_index]
		test_precision_for_best_test_accuracy = cv_results['test_precision'][best_test_accuracy_index]
		
		train_recall_for_best_test_accuracy = cv_results['train_recall'][best_test_accuracy_index]
		test_recall_for_best_test_accuracy = cv_results['test_recall'][best_test_accuracy_index]
		
		train_roc_for_best_test_accuracy = cv_results['train_roc'][best_test_accuracy_index]
		test_roc_for_best_test_accuracy = cv_results['test_roc'][best_test_accuracy_index]
		
		
		# best train_precision
		best_train_precision_index = np.argmax(cv_results['train_precision'])
		
		best_train_precision = cv_results['train_precision'][best_train_precision_index]
		test_precision_for_best_train_precision = cv_results['test_precision'][best_train_precision_index]
		
		train_accuracy_for_best_train_precision = cv_results['train_accuracy'][best_train_precision_index]
		test_accuracy_for_best_train_precision = cv_results['test_precision'][best_train_precision_index]
		
		test_recall_for_best_train_precision = cv_results['test_recall'][best_train_precision_index]
		train_recall_for_best_train_precision = cv_results['train_recall'][best_train_precision_index]
		
		train_roc_for_best_train_precision = cv_results['train_roc'][best_train_precision_index]
		test_roc_for_best_train_precision = cv_results['test_roc'][best_train_precision_index]
		
		
		# best test_precision
		best_test_precision_index = np.argmax(cv_results['test_precision'])
		
		best_test_precision = cv_results['test_precision'][best_test_precision_index]
		train_precision_for_best_test_precision = cv_results['train_precision'][best_test_precision_index]
		
		train_accuracy_for_best_test_precision = cv_results['train_accuracy'][best_test_precision_index]
		test_accuracy_for_best_test_precision = cv_results['test_precision'][best_test_precision_index]
		
		test_recall_for_best_test_precision = cv_results['test_recall'][best_test_precision_index]
		train_recall_for_best_test_precision = cv_results['train_recall'][best_test_precision_index]
		
		train_roc_for_best_test_precision = cv_results['train_roc'][best_test_precision_index]
		test_roc_for_best_test_precision = cv_results['test_roc'][best_test_precision_index]
		
		
		# best train_recall
		best_train_recall_index = np.argmax(cv_results['train_recall'])
		
		best_train_recall = cv_results['train_recall'][best_train_recall_index]
		test_recall_for_best_train_recall = cv_results['test_recall'][best_train_recall_index]
		
		train_precision_for_best_train_recall = cv_results['train_precision'][best_train_recall_index]
		test_precision_for_best_train_recall = cv_results['test_precision'][best_train_recall_index]
		
		train_accuracy_for_best_train_recall = cv_results['train_accuracy'][best_train_recall_index]
		test_accuracy_for_best_train_recall = cv_results['test_precision'][best_train_recall_index]
		
		train_roc_for_best_train_recall = cv_results['train_roc'][best_train_recall_index]
		test_roc_for_best_train_recall = cv_results['test_roc'][best_train_recall_index]
		
		
		# best test_recall
		best_test_recall_index = np.argmax(cv_results['test_recall'])
		
		best_test_recall = cv_results['test_recall'][best_test_recall_index]
		train_recall_for_best_test_recall = cv_results['train_recall'][best_test_recall_index]
		
		train_precision_for_best_test_recall = cv_results['train_precision'][best_test_recall_index]
		test_precision_for_best_test_recall = cv_results['test_precision'][best_test_recall_index]
		
		train_accuracy_for_best_test_recall = cv_results['train_accuracy'][best_test_recall_index]
		test_accuracy_for_best_test_recall = cv_results['test_precision'][best_test_recall_index]
		
		train_roc_for_best_test_recall = cv_results['train_roc'][best_test_recall_index]
		test_roc_for_best_test_recall = cv_results['test_roc'][best_test_recall_index]
		
		
		# best train_roc
		best_train_roc_index = np.argmax(cv_results['train_roc'])
		
		best_train_roc = cv_results['train_roc'][best_train_roc_index]
		test_roc_for_best_train_roc = cv_results['test_roc'][best_train_roc_index]
		
		train_recall_for_best_train_roc = cv_results['train_recall'][best_train_roc_index]
		test_recall_for_best_train_roc = cv_results['test_recall'][best_train_roc_index]
		
		train_precision_for_best_train_roc = cv_results['train_precision'][best_train_roc_index]
		test_precision_for_best_train_roc = cv_results['test_precision'][best_train_roc_index]
		
		train_accuracy_for_best_train_roc = cv_results['train_accuracy'][best_train_roc_index]
		test_accuracy_for_best_train_roc = cv_results['test_precision'][best_train_roc_index]
		
		
		# best test_roc
		best_test_roc_index = np.argmax(cv_results['test_roc'])
		
		best_test_roc = cv_results['test_roc'][best_test_roc_index]
		train_roc_for_best_test_roc = cv_results['train_roc'][best_test_roc_index]
		
		train_precision_for_best_test_roc = cv_results['train_precision'][best_test_roc_index]
		test_precision_for_best_test_roc = cv_results['test_precision'][best_test_roc_index]
		
		train_accuracy_for_best_test_roc = cv_results['train_accuracy'][best_test_roc_index]
		test_accuracy_for_best_test_roc = cv_results['test_precision'][best_test_roc_index]
		
		train_recall_for_best_test_roc = cv_results['train_recall'][best_test_roc_index]
		test_recall_for_best_test_roc = cv_results['test_recall'][best_test_roc_index]
		
		
		indices = ['Train Accuracy', 'Test Accuracy', 'Train Precision', 'Test Precision', 'Train Recall', 'Test Recall', 'Train ROC', 'Test ROC']
		columns = ['Index', 'Best', 'Train Accuracy', 'Test Accuracy', 'Train Precision', 'Test Precision', 'Train Recall', 'Test Recall', 'Train ROC', 'Test ROC']
					
		d = [
			 [ best_train_accuracy_index, best_train_accuracy, 
				best_train_accuracy, test_accuracy_for_best_train_accuracy, 
				train_precision_for_best_train_accuracy, test_precision_for_best_train_accuracy, 
				train_recall_for_best_train_accuracy, test_recall_for_best_train_accuracy, 
				train_roc_for_best_train_accuracy, test_roc_for_best_train_accuracy ],
			 
			 [ best_test_accuracy_index, best_test_accuracy, 
				train_accuracy_for_best_test_accuracy, best_test_accuracy, 
				train_precision_for_best_test_accuracy, test_precision_for_best_test_accuracy, 
				train_recall_for_best_test_accuracy, test_recall_for_best_test_accuracy, 
				train_roc_for_best_test_accuracy, test_roc_for_best_test_accuracy ],
			 
			 [ best_train_precision_index, best_train_precision, 
				train_accuracy_for_best_train_precision, test_accuracy_for_best_train_precision, 
				best_train_precision, test_precision_for_best_train_precision, 
				train_recall_for_best_train_precision, test_recall_for_best_train_precision, 
				train_roc_for_best_train_precision, test_roc_for_best_train_precision ],
			 
			 [ best_test_precision_index, best_test_precision, 
				train_accuracy_for_best_test_precision, test_accuracy_for_best_test_precision, 
				train_precision_for_best_test_precision, best_test_precision, 
				train_recall_for_best_test_precision, test_recall_for_best_test_precision, 
				train_roc_for_best_test_precision, test_roc_for_best_test_precision ],
			 
			 [ best_train_recall_index, best_train_recall, 
				train_accuracy_for_best_train_recall, test_accuracy_for_best_train_recall, 
				train_precision_for_best_train_recall, test_precision_for_best_train_recall, 
				best_train_recall, test_recall_for_best_train_recall, 
				train_roc_for_best_train_recall, test_roc_for_best_train_recall ],
			 
			 [ best_test_recall_index, best_test_recall, 
				train_accuracy_for_best_test_recall, test_accuracy_for_best_test_recall, 
				train_precision_for_best_test_recall, test_precision_for_best_test_recall, 
				train_recall_for_best_test_recall, best_test_recall, 
				train_roc_for_best_test_recall, test_roc_for_best_test_recall ],
				
			 [ best_train_roc_index, best_train_roc, 
				train_accuracy_for_best_train_roc, test_accuracy_for_best_train_roc, 
				train_precision_for_best_train_roc, test_precision_for_best_train_roc, 
				train_recall_for_best_train_roc, test_recall_for_best_train_roc, 
				best_train_roc, test_roc_for_best_train_roc ],
			 
			 [ best_test_roc_index, best_test_roc, 
				train_accuracy_for_best_test_roc, test_accuracy_for_best_test_roc, 
				train_precision_for_best_test_roc, test_precision_for_best_test_roc, 
				train_recall_for_best_test_roc, test_recall_for_best_test_roc, 
				train_roc_for_best_test_roc, best_test_roc ],
			]
		
		df = pd.DataFrame(d, index = indices, columns = columns)
		
		display_func("-> " + estimator_name + " scores") 
		display_func(df) # to format output similar to Jupyter's output
		
		# print(cv_results.keys())
	else:
		display_func("Estimator Type not specificed", mode=__PRINT)
		print_separator()
		return
	
	print_separator()
	# print(cv_results.keys())
	
	return cv_results

def print_confusion_matrix(y_true, y_pred):
	"""Prints the confision matrix with columns and index
	
    Args:
		y_true (Union[ndarray, pd.Series]): Actual Response
		y_pred (Union[ndarray, pd.Series]): Predicted Response
		
    """
	
	cfm_i = pd.DataFrame(confusion_matrix(y_true, y_pred))
	cfm_columns = []
	cfm_index = []
	for each_class in np.unique(y_true):
		cfm_columns.append("Predicted Class: " + str(each_class))
		cfm_index.append("Actual Class: " + str(each_class))
		
	cfm_i.columns = cfm_columns
	cfm_i.index = cfm_index
	display_func("-> Confusion Matrix", mode=__PRINT)
	display_func(cfm_i,mode=None)

def plot_decision_boundary(x_axis_data, y_axis_data, response, estimator):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	plt.figure(figsize=(12,6))
	plt.scatter( x_axis_data, y_axis_data, c=response, cmap=plt.cm.Paired )
	h = .02  # step size in the mesh
	# create a mesh to plot in
	x_min, x_max = x_axis_data.min() - 1, x_axis_data.max() + 1
	y_min, y_max = y_axis_data.min() - 1, y_axis_data.max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

	# Plot the decision boundary. For that, we will assign a color to each
	# point in the mesh [x_min, m_max]x[y_min, y_max].
	Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.contour(xx, yy, Z, cmap=plt.cm.Paired)

# def plot_roc_curve(estimator, X_test, y_test, classes):
	# y_pred = estimator.predict(X_test)
	# fpr, tpr, thresholds = roc_curve(y_test, y_pred)
	# roc_auc = roc_auc_score(y_test, y_pred)
	# Plot ROC curve
	# plt.figure()
	# plt.figure(figsize=(12,6))
	# lw = 2
	# plt.plot(fpr, tpr, label='ROC curve, area = %0.5f' % roc_auc)
	# plt.plot([0, 1], [0, 1], 'k--')  # random predictions curve
	# plt.xlim([0.0, 1.0])
	# plt.ylim([0.0, 1.0])
	# plt.xlabel('False Positive Rate')
	# plt.ylabel('True Positive Rate')
	# plt.title('Receiver Operating Characteristic')

# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
def plot_roc_curve(estimator, X_train, X_test, y_train, y_test, classes):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	num_of_classes = len(classes)
	if(num_of_classes < 2):
		print("Number of classes have to be greater than or equal to 2")
		return None
	
	# typicall classes are 0,1 or -1, 1 in two class responses. if not then will this work?
	if(num_of_classes == 2):
		classifier = OneVsRestClassifier(estimator)
		y_pred = classifier.fit(X_train, y_train).predict(X_test)
		fpr, tpr, thresholds = roc_curve(y_test, y_pred)
		roc_auc = roc_auc_score(y_test, y_pred)
		lw = 2
		plt.figure(figsize=(12,6))
		plt.plot(fpr, tpr, lw=2)
		plt.plot([0, 1], [0, 1], linestyle='--', lw=lw)  # random predictions curve
		plt.xlim([-0.001, 1.0])
		plt.ylim([0.0, 1.05])
		plt.xlabel('False Positive Rate')
		plt.ylabel('True Positive Rate')
		plt.title('ROC curve (area = %0.3f)' %roc_auc)
		return fpr, tpr, roc_auc

	# when number of classes is more than 2 then
	
	# Binarize the output
	y_test = label_binarize(y_test, classes=classes) # converts 3 classes in one column to 3 columns binary matrix
	num_of_classes = y_test.shape[1]

	# Learn to predict each class against the other
	classifier = OneVsRestClassifier(estimator)
	
	# as of now found that SVM only has the decision_function implemented
	if hasattr(classifier, "decision_function"):
		y_pred = classifier.fit(X_train, y_train).decision_function(X_test)
	else:
		y_pred = classifier.fit(X_train, y_train).predict_proba(X_test)
	
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	for i in range(num_of_classes):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pred[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

	# Compute micro-average ROC curve and ROC area
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_pred.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	
	plot_roc_curve_multiclass(fpr, tpr, roc_auc, classes)
	
	return fpr, tpr, roc_auc

def plot_roc_curve_multiclass(fpr, tpr, roc_auc, classes):
	"""Summary line.

    Extended description of function.

    Args:
        
		
    """
	
	# Compute macro-average ROC curve and ROC area

	num_of_classes = len(classes)
	
	# First aggregate all false positive rates
	all_fpr = np.unique(np.concatenate([fpr[i] for i in range(num_of_classes)]))

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
	plt.title('Some extension of Receiver operating characteristic to multi-class')
	plt.legend(loc="lower right")
	plt.show()
