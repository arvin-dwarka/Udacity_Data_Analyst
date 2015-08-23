import numpy as np
import pandas
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import statsmodels.api as sm
from datetime import *



# ps3.1
def entries_histogram(turnstile_weather):
	'''
	This function plot two histograms on the same axes to show hourly
	entries when raining vs. when not raining.
	'''
	plt.figure()
	turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0].hist(bins=200, alpha=0.75)
	turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1].hist(bins=200, alpha=0.75)

	plt.axis([0, 6000, 0, 45000])
	plt.suptitle('Histogram of ENTRIESn_hourly')
	plt.xlabel('ENTRIESn_hourly')
	plt.ylabel('Frequency')
	plt.legend(['No rain', 'Rain'])

	return plt

# ps3.3
def mann_whitney_plus_means(turnstile_weather):
	'''
	This function returns the means of entries with and without rain,
	and the Mann-Whitney U-statistic.
	'''
	with_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1]
	without_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0]
	with_rain_mean = with_rain.mean()
	without_rain_mean = without_rain.mean()

	U, p = scipy.stats.mannwhitneyu(with_rain, without_rain)

	return with_rain_mean, without_rain_mean, U, p

# ps3.5
def linear_regression(features, values):
	"""
	This function performs linear regression given a data set with
	an arbitrary number of features.
	"""
	features = sm.add_constant(features)
	model = sm.OLS(values, features)
	results = model.fit()
	intercept = results.params[0]
	params = results.params[1:]

	return intercept, params

# ps3.6
def plot_residuals(turnstile_weather, predictions):
	'''
	This function plots a histogram of entries per hour for our data, for
	the difference between the original hourly entry data and the predicted values
	'''
	plt.figure()
	(turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins=200)
	plt.suptitle('Residual histogram')
	plt.xlabel('Residuals')
	plt.ylabel('Frequency')
	return plt

# ps3.7
def compute_r_squared(data, predictions):
	'''
	This function computes the R-squared for predictions.
	'''
	r_squared = 1-(np.sum(np.square(data-predictions)))/ \
	np.sum(np.square(data-np.mean(data)))
	return r_squared

# ps3.8
def normalize_features(features):
	''' 
	This function returns the means and standard deviations of the given features,
	along with a normalized feature matrix.
	''' 
	means = np.mean(features, axis=0)
	std_devs = np.std(features, axis=0)
	normalized_features = (features - means) / std_devs
	return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
	''' 
	This function recovers the weights for a linear model given parameters that
	were fitted using normalized features. Takes the means and standard
	deviations of the original features, along with the intercept and
	parameters computed using the normalized features, and returns the
	intercept and parameters that correspond to the original features.
	''' 
	intercept = norm_intercept - np.sum(means * norm_params / std_devs)
	params = norm_params / std_devs
	return intercept, params

def predictions(dataframe):
	'''
	This function runs preductions on dataframe via gradient descent.
	'''
	dataframe['weekday'] = dataframe['DATEn'].map(lambda x:datetime.strptime(x, '%Y-%m-%d').weekday())
	features = dataframe[['rain', 'precipi', 'meanwindspdi', 'Hour', 'meantempi', 'weekday']]
	dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
	features = features.join(dummy_units)

	# Values
	values = dataframe['ENTRIESn_hourly']

	# Get numpy arrays
	features_array = features.values
	values_array = values.values

	means, std_devs, normalized_features_array = normalize_features(features_array)

	# Perform gradient descent
	norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
	intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
	predictions = intercept + np.dot(features_array, params)

	return predictions

if __name__ == '__main__':
	df = pandas.DataFrame.from_csv('turnstile_data_master_with_weather.csv')

	print entries_histogram(df)
	plt.show()
	raw_input("Press enter to continue...")

	print "Mann-Whitney U test:"
	print mann_whitney_plus_means(df)
	raw_input("Press enter to continue...")

	print "Linear regression predictions via gradient descent:"
	predictions = predictions(df)
	print predictions
	raw_input("Press enter to continue...")

	print "Plotting residuals:"
	plot_residuals(df, predictions)
	plt.show()
	raw_input("Press enter to continue...")

	print "R-squared value:"
	print compute_r_squared(df['ENTRIESn_hourly'], predictions)
