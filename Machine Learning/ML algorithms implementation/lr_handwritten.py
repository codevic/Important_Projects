# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:36:27 2017

@author: kavya
"""
import numpy as np
import pandas as pd
from sklearn.cross_validation import KFold

HandWritten = pd.read_csv('HandWrittenLetters.txt',header = -1).as_matrix();
#ATNTfile = pd.read_csv('ATNTFaceImages400.txt',header = -1).as_matrix();

Xdata = np.transpose(HandWritten[1:321,:])
Ydata = np.transpose(HandWritten[0,:])

print(Xdata.shape)
print(Ydata.shape)

kf = KFold(len(Ydata), n_folds=5, shuffle=True)
print(kf)

'''Looping thorught the kfold to access every index of that feature one at a time.'''
for train_index, test_index in kf:
   X_train, X_test = Xdata[train_index], Xdata[test_index]
   y_train, y_test = Ydata[train_index], Ydata[test_index]

'''
print(X_train)
print(y_train)
print(y_test)
print(X_test)'''
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)
N_train = 812
N_test = 202

A_train = np.ones((1,N_train))    # N_train : number of training instance
A_test = np.ones((1,N_test))      # N_test  : number of test instance
print(A_train.shape)
print(A_test.shape)
X_train = np.transpose(X_train)
y_train = np.transpose(y_train)
y_test = np.transpose(y_test)
X_test = np.transpose(X_test)
X_train_padding = np.row_stack((X_train,A_train))
X_test_padding = np.row_stack((X_test,A_test))
print(X_train_padding.shape)
print(X_test_padding.shape)

#computing the regression coefficients
B_padding = np.dot(np.linalg.pinv(np.transpose(X_train_padding)), np.transpose(y_train))   # (XX')^{-1} X  * Y'  #Ytrain : indicator matrix
print(B_padding)
print("--------------")
y_test_padding = np.dot(B_padding.T,X_test_padding)
print(y_test_padding)
print("--------------")
y_test_padding_argmax = np.argmax(y_test_padding,axis=0)+1
print(y_test_padding_argmax)
print("--------------")
err_test_padding = y_test - y_test_padding_argmax
print(err_test_padding)
print("--------------")
TestingAccuracy_padding = (1-np.nonzero(err_test_padding)[0].size/len(err_test_padding))*100
print(TestingAccuracy_padding)
print("--------------")