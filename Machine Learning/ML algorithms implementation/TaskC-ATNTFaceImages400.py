# -*- coding: utf-8 -*-
"""
@author: kavya
"""

import pandas as pd
import numpy as np

'''Reading the input file and converting it to matrix'''
file = pd.read_csv('ATNTFaceImages400.txt', header = -1)
data = file.as_matrix()
print(data.shape)

'''Splitting the features and labels from the first line of the matrix 
    and transposing it to achieve the appropriate dimension'''
    
X_train = data[1:,0:9]
y_train = data[0:1,0:9]
    
X_test = data[1:,9]
y_test = data[0:1,9]
print(X_train.shape)
print(X_test.shape)
'''Splitting the features and labels from the next lines of the matrix 
    and transposing it to achieve the appropriate dimension.
    Horizontally contcatenate the matrices'''
i = 1
while(i<=390):
    X_train = np.hstack((X_train,data[1:,i:i+9]))
    y_train = np.hstack((y_train,data[0:1,i+9:i+18]))
    
    X_test = np.hstack((X_test,data[1:,i+9]))
    y_test = np.hstack((y_test,data[0:1,i+9]))
    i+=10
    
'''Printing the test and train data'''
print("y_train: ",y_train.shape)
print("X_train: ",X_train.shape)
print("y_test: ",y_test.shape)
print("X_test: ",X_test.shape)