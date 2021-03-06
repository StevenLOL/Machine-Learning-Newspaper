# -*- coding: UTF-8 -*-

import numpy as np
from sklearn.cross_validation import KFold
from sklearn.linear_model import LinearRegression, ElasticNet, Lasso, Ridge, ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif, chi2
from sklearn.feature_selection import SelectKBest, f_regression
import pickle
from sklearn import preprocessing
from sklearn import cross_validation
import matplotlib.pyplot as plt
from itertools import cycle



def preprocess(article_file, lable_file):

    features = pickle.load(open(article_file))
    features = np.array(features)

    # transform non-numerical labels (as long as they are hashable and comparable) to numerical labels
    lables = pickle.load(open(lable_file))
    le = preprocessing.LabelEncoder()
    le.fit(lables)
    lables = le.transform(lables)
    # print le.inverse_transform([0])

    ### text vectorization--go from strings to lists of numbers
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=1,
                                 stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features)

    # selector : chi2
    selector = SelectPercentile(score_func=chi2)
    selector.fit(features_train_transformed, lables)

    features_train_transformed = selector.transform(features_train_transformed).toarray()

    return features_train_transformed, lables, vectorizer, selector, le, features



data = {}


features, labels, vectorizer, selector, le, features_data = preprocess("pkl/article_2_people.pkl", "pkl/lable_2_people.pkl")
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.1, random_state=42)

for name, clf in [
    ('linear regression', LinearRegression(fit_intercept=True)),
    ('lasso()', Lasso()),
    ('elastic-net(.5)', ElasticNet(alpha=0.5)),
    ('lasso(.5)', Lasso(alpha=0.5)),
    ('ridge(.5)', Ridge(alpha=0.5))
]:

    if not data.has_key(name):
        data[name] = []

    print "*" * 100
    print('Method: {}'.format(name))

    # Fit on the whole data:
    t0 = time()
    clf.fit(features_train, labels_train)
    print ("training time:", round(time()-t0, 3), "s")

    # Predict on the whole data:
    y_pred = clf.predict(features_test)
    print ("predicting time:", round(time()-t0, 3), "s")

    score_accuracy = mean_squared_error(y_pred, labels_test)
    print('r2 score : {}'.format(r2_score(y_pred, labels_test)))
    print('mean squared error : {}'.format(score_accuracy))

    print "*"* 100

    data[name].append(score_accuracy)


print data