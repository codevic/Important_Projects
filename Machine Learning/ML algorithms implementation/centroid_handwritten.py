# -*- coding: utf-8 -*-
"""
@author: kavya
"""

import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.cross_validation import KFold

'''Reading the input file and converting it to matrix'''
file = pd.read_csv('HandWrittenLetters.txt', header = -1)
data = file.as_matrix()

'''Splitting the features and labels from the matrix 
    and transposing it to achieve the appropriate dimension'''
X = np.transpose(data[1:321,:])
y = np.transpose(data[0,:])
print(X.shape)
print(y.shape)

'''Splitting the data for kfold cross valaidation using KFold() method'''
kf = KFold(len(y), n_folds=5, shuffle=True)
print(kf)

'''Looping thorught the kfold to access every index of that feature one at a time.'''
for train_index, test_index in kf:
   X_train, X_test = X[train_index], X[test_index]
   y_train, y_test = y[train_index], y[test_index]
   print(X_train.shape)
   print(y_train.shape)
   '''Performing Centroid to classify each feature tot he correspoding label.'''
   #Centroid Classification
   centroid_classifier = NearestCentroid()
   # Train the model using the training sets
   centroid_classifier.fit(X_train, y_train)
   # Predict the labels
   predictions = centroid_classifier.predict(X_test)
   
   '''Calculating the accuracy between the actual label and predicted label in percentage[(accuracy*100)%]'''
   actual = y_test 
   accuracy = metrics.accuracy_score(actual,predictions) * 100
   print("Accuracy is: ",accuracy)
