import numpy as np
import pandas
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import statsmodels.api as sm


# ps3.1
def entries_histogram(turnstile, csv=False):
	'''
	This function plot two histograms on the same axes to show hourly
	entries when raining vs. when not raining.
	'''
	if csv:
		turnstile_weather = pandas.read_csv(turnstile_weather)
	else:
		turnstile_weather = turnstile

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
def mann_whitney_plus_means(turnstile_weather, csv=False):
	'''
	This function returns the means of entries with and without rain,
	and the Mann-Whitney U-statistic.
	'''
	if csv:
		df = pandas.read_csv(turnstile_weather)
	else:
		df = turnstile_weather

	with_rain = df['ENTRIESn_hourly'][df['rain'] == 1]
	without_rain = df['ENTRIESn_hourly'][df['rain'] == 0]
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
	r_squared = 1-(np.sum(np.square(data-predictions)))/np.sum(np.square(data-np.mean(data)))
	return r_squared



