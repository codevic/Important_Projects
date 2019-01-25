# -*- coding: utf-8 -*-
"""
@author: kavya
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.cross_validation import KFold

'''Reading the input file and converting it to matrix'''
file = pd.read_csv('ATNTFaceImages400.txt', header = -1)
data = file.as_matrix()

'''Splitting the features and labels from the matrix 
    and transposing it to achieve the appropriate dimension'''
X = np.transpose(data[1:645,:])
y = np.transpose(data[0,:])
#print(X)
#print(y)

'''Splitting the data for kfold cross valaidation using KFold() method'''
kf = KFold(len(y), n_folds=5, shuffle=True)
print(kf)

'''Looping thorught the kfold to access every index of that feature one at a time.'''
for train_index, test_index in kf:
   X_train, X_test = X[train_index], X[test_index]
   y_train, y_test = y[train_index], y[test_index]

   '''Performing Linear Regression to classify each feature tot he correspoding label.'''
   #Linear Regression
   regr = linear_model.LogisticRegression()
   # Train the model using the training sets
   regr.fit(X_train, y_train)
   # Predict the labels
   predictions = regr.predict(X_test)
   
   '''Calculating the accuracy between the actual label and predicted label in percentage[(accuracy*100)%]'''
   actual = y_test
   accuracy = r2_score(actual, predictions) * 100
   print("Mean squared error: %.2f" % mean_squared_error(actual, predictions))
   print("Variance score : ", accuracy)
