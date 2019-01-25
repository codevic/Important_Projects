# this code is taken from an online github repositort and the necessary modifications have been made with respect to the project requirements
#!/usr/bin/env python
#import pdb
import pandas as pd
from random import randrange
import random
import numpy as np
from c45 import C45

def createAndStoreData(data, filename):
        file = open(filename,"w")
        rx,cx = data.shape
        for i in range(0,rx):
            for j in range(0,cx):
                file.write(str(data[i][j]))
                if(j<cx-1):
                    file.write(',')
            file.write("\n")
        file.close()
    
def cross_validation_split(dataset, folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / folds)
	for i in range(folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index)) 
		dataset_split.append(fold)
	return dataset_split


def c45_using_kfold(dataset, k):
    folds = np.array(cross_validation_split(dataset, k))
    rx, cx = dataset.shape
    sum = 0
    for i in range(0, k):
        train_data = np.zeros((1, cx))
        test_data = folds[i]
        for j in range(0, k):
            if i != j:
                train_data = np.concatenate((train_data, folds[j]))
        train_data = train_data[1:, :]
        createAndStoreData(train_data, "../data/iris/trainData.data")
        c1 = C45("../data/iris/trainData.data", "../data/iris/iris.names")
        c1.getData()
        c1.preprocessData()
        c1.createTree()
        print("Tree ",i,": -------------------------------------------------")
        c1.printTree()
        accuracy = c1.calc_accuracy(test_data)
        print(accuracy)
        sum += accuracy
    average_accuracy = sum / k
    print("Average accuracy : ", average_accuracy)


def c45_using_80_20_dataSplitting(dataset):
    rx, cx = dataset.shape
    train_data = dataset[:int((len(dataset) + 1) * .80)]  # Remaining 80% to training set
    test_data = dataset[int((len(dataset) + 1) * .80 + 1):]  # Splits 20% data to test set
    createAndStoreData(train_data, "../data/iris/trainData.data")
    c1 = C45("../data/iris/trainData.data", "../data/iris/iris.names")
    c1.getData()
    c1.preprocessData()
    c1.createTree()
    print("Tree : -------------------------------------------------")
    c1.printTree()
    print("Accuracy: ", c1.calc_accuracy(test_data))


dataset = pd.read_csv('../data/iris/iris.data', header=-1).as_matrix()
k = 5
random.shuffle(dataset)
print("--------------------------------------------------------")
print("Decision tree prediction using k fold cross validation:")
c45_using_kfold(dataset,k)
print("--------------------------------------------------------")
print("Decision tree prediction using 80-20 data split:")
c45_using_80_20_dataSplitting(dataset)
print("--------------------------------------------------------")