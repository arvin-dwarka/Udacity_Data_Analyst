#!/usr/bin/python

import sys
import pickle
sys.path.append("tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from pprint import pprint
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV

import helper

### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
poi_label = ['poi']

financial_features_list = [
	'salary', 
	'deferral_payments', 
	'total_payments', 
	'loan_advances', 
	'bonus', 
	'restricted_stock_deferred', 
	'deferred_income', 
	'total_stock_value', 
	'expenses', 
	'exercised_stock_options', 
	'other', 
	'long_term_incentive', 
	'restricted_stock', 
	'director_fees'
	]

email_features_list = [
	'to_messages', 
	#'email_address', 
	'from_poi_to_this_person', 
	'from_messages', 
	'from_this_person_to_poi',
	'shared_receipt_with_poi'
	]

features_list = poi_label + financial_features_list + email_features_list

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### Remove outliers
outlier_keys = ['TOTAL', 'LOCKHART EUGENE E', 'THE TRAVEL AGENCY IN THE PARK']
helper.remove_keys(data_dict, outlier_keys)

### Store to my_dataset for easy export below.
my_dataset, my_feature_list = data_dict, features_list

### Create new feature - total_compensation - since money is a key motivator for fraud
new_feature_list = ['salary', 'bonus', 'total_stock_value']
for record in my_dataset:
    person = data_dict[record]
    is_NaN = False
    for field in new_feature_list:
        if person[field] == 'NaN':
            is_NaN = True
    if is_NaN:
        person['total_compensation'] = 'NaN'
    else:
        person['total_compensation'] = sum([person[feature] for feature in new_feature_list])
my_feature_list += ['total_compensation']

### Optimize feature selection
best_features = helper.k_best(my_dataset, my_feature_list, k=15)
my_feature_list = poi_label + best_features.keys()
my_feature_list = ['poi','salary','exercised_stock_options', 'bonus'] #surprisingly, this gave the best results!

### Visualize features for exploratory data analysis - commented out to speed through ML algorithms
#helper.plot(my_dataset, 'salary', 'exercised_stock_options')

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, my_feature_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
features = MinMaxScaler().fit_transform(features)
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3)

# print features used
print "{0} selected features: {1}\n".format(len(my_feature_list) - 1, my_feature_list[1:])


names = [
    "Nearest Neighbors", 
    "K-Means", 
    "Linear SVM", 
    "RBF SVM", 
    "Decision Tree",
    "Random Forest", 
    "AdaBoost", 
    "Naive Bayes", 
    "LDA", 
    "QDA", 
    "Logistic Regression"
    ]

classifiers = [
    KNeighborsClassifier(n_neighbors=3),
    KMeans(),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    GaussianNB(),
    LDA(),
    QDA(),
    LogisticRegression()
    ]

for name, clf in zip(names, classifiers):
        clf.fit(features_train, labels_train)
        pred = clf.predict(features_test)
        prec = precision_score(labels_test, pred)
        recall = recall_score(labels_test, pred)
        helper.clf_evaluator(clf, features, labels)


### Tune KNeighborsClassifier
cv = StratifiedShuffleSplit(labels, 1000, random_state = 42)
metrics = ['minkowski', 'euclidean', 'manhattan'] 
weights = ['uniform', 'distance']
n_neighbors = [1,2,3,4,5,6,7,8,9,10]
param_grid_knc = dict(metric=metrics, weights=weights, n_neighbors=n_neighbors)
clf_knc = GridSearchCV(KNeighborsClassifier(), param_grid=param_grid_knc, cv=cv)
clf_knc.fit(features, labels)
print clf_knc.best_estimator_
print clf_knc.best_score_

### Tune KMeans
n_clusters = [2,3,4,5,6,7,8]
tol = [0.000001, 0.00001, 0.0001, 0.001]
param_grid_km = dict(n_clusters=n_clusters, tol=tol)
clf_km = GridSearchCV(KMeans(), param_grid=param_grid_km, cv=cv)
clf_km.fit(features, labels)
print clf_km.best_estimator_
print clf_km.best_score_


clf = KNeighborsClassifier(n_neighbors=3)

### Dump your classifier, dataset, and features_list and 
### generate the necessary .pkl files for validating results
pickle.dump(my_dataset, open("my_dataset.pkl", "w"))
pickle.dump(clf, open("my_classifier.pkl", "w"))
pickle.dump(my_feature_list, open("my_feature_list.pkl", "w"))