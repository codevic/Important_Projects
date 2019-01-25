# -*- coding: utf-8 -*-
"""
@author: kavya
"""

import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier

'''Reading the input file and converting it to matrix'''
file = pd.read_csv('HandWrittenLetters.txt', header = -1)
data = file.as_matrix()
print(data.shape)
'''Splitting the features and labels pertaining to 'C' and 'F' from the matrix 
    and transposing it to achieve the appropriate dimension'''

C_X_train = data[1:,78:108]
C_X_test = data[1:,108:117]

C_y_train = data[0:1,78:108]
C_y_test = data[0:1,108:117]

F_X_train = data[1:,195:225]
F_X_test = data[1:,225:234]

F_y_train = data[0:1,195:225]
F_y_test = data[0:1,225:234]

X_train = np.transpose( np.hstack((C_X_train,F_X_train)))
print("X_train: ",X_train)

Y_train = np.transpose(np.hstack((C_y_train,F_y_train)))
y = Y_train.ravel()
Y_train = np.array(y).astype(int)
print("y_train: ",Y_train)

X_test = np.hstack((C_X_test,F_X_test))
print("X_test: ",X_test)

Y_test = np.hstack((C_y_test,F_y_test))
print("y_test: ",Y_test)

knneighbors = KNeighborsClassifier(n_neighbors=3)
# Train the model using the training sets
knneighbors.fit(X_train, Y_train)
# Predict the labels
predictions = knneighbors.predict(X_test)
#print(predictions)

'''Using 2 class SVM classifier (One-against-one classifier)
clf = svm.SVC(decision_function_shape='ovo')
clf.fit(X_train, Y_train)
dec = clf.decision_function(np.transpose(X_test))
predictions = clf.predict(np.transpose(X_test))
#print(dec)
#print(predictions)
Calculating the accuracy between the actual label and predicted label in percentage[(accuracy*100)%]
actual = np.transpose(Y_test)
accuracy = r2_score(actual, predictions) * 100
print("Accuracy is: ",accuracy)
'''