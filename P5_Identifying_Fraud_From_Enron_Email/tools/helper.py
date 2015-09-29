import matplotlib.pyplot as plt
import pickle
import sys
import itertools
import csv

from feature_format import featureFormat
from feature_format import targetFeatureSplit
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_selection import SelectKBest
from numpy import mean
from pprint import pprint

def remove_keys(data_dict, keys):
    '''
    Removes a list of keys from a dictionary object

    Params:
        data_dict - input dictionary
        keys - list of keys to be removed

    Return:
        A modified dictionary without the listed keys
    '''
    for k in keys:
        data_dict.pop(k, 0)
    return data_dict

def plot(data_dict, x_data, y_data):
    """
    Generates a plot of the distribution of y_data over x_data, split by POIs

    Params:
        data_dict - input dictionary
        x_data - x-axis data points
        y_data - y-axis data points
    """
    data = featureFormat(data_dict, [x_data, y_data, 'poi'])

    for value in data:
        x = value[0]
        y = value[1]
        poi = value[2]
        color = 'blue' if poi else 'grey'
        plt.scatter(x, y, color=color)
    plt.xlabel(x_data)
    plt.ylabel(y_data)
    plt.show()

def clf_evaluator(clf, features, labels, iterations=1000, test_size=0.3):
    '''
    Evaluates the ML algorithm's performance

    Params:
        clf - ML algorithm
        features - list of features
        labels - list of labels
        iterations - number of times this function will iterate through (default is 1,000)
        test_size - size of cross validation split

    Print:
        Mean of accuracy, precision and recall
	'''
    print clf
    accuracy, precision, recall = [], [], []
    for i in range(iterations):
        features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=test_size)
        clf.fit(features_train, labels_train)
        pred = clf.predict(features_test)
        accuracy.append(accuracy_score(labels_test, pred))
        precision.append(precision_score(labels_test, pred, average="weighted"))
        recall.append(recall_score(labels_test, pred, average="weighted"))

    print "accuracy: {}".format(mean(accuracy))
    print "precision: {}".format(mean(precision))
    print "recall: {}\n".format(mean(recall))

def k_best(data_dict, features_list, k):
    '''
    Identify the best features to use in ML algorithms

    Params:
        data_dict - input dictionary
        features_list - list of features to test
        k - totol number of top features to select from features_list

    Return:
        A dictionary of best features
    '''
    data = featureFormat(data_dict, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    #combine features and scores, and sort in descending order
    feature_score_pairs = list(sorted(zip(features_list[1:], scores), key=lambda x: x[1], reverse=True))
    best_features = dict(feature_score_pairs[:k])

    #pprint(feature_score_pairs)
    return best_features

def percent_invalid(data_dict, features_list):
    '''
    Calculate the percentage of invalid or NaN values are in the dataset

    Params:
        data_dict - input dictionary
        features_list - list of features_list to test

    Return:
        Percentage of invalid or NaN values for the selected features
    '''
    NaN_counts = dict.fromkeys(data_dict.itervalues().next().keys(), 0)
    valid_counts = NaN_counts
    percent_invalid = dict(itertools.izip_longest(*[iter(features_list)] * 2, fillvalue=""))

    for record in data_dict:
        person = data_dict[record]
        for field in person:
            if person[field] == 'NaN':
                NaN_counts[field] += 1
            else:
                valid_counts[field] += 1
    for feature in features_list:
        percent_invalid[feature] = 100.0 * float(NaN_counts[feature],2)/float(NaN_counts[feature]+valid_counts[feature], 2)
    
    return percent_invalid