# this code is taken from an online github repositort and the necessary modifications have been made with respect to the project requirements
import math
class C45:
    
    def __init__(self, dataPath, namesPath):
        self.dataPath = dataPath
        self.namesPath = namesPath
        self.data = []
        self.classes = []
        self.tree = None
        self.numberOfAttr = -1
        self.valuesOfAttr = {}
        self.attributes = []

    def getData(self):
        with open(self.namesPath, "r") as file:
            classes = file.readline()
            self.classes = [x.strip() for x in classes.split(",")]
            #add attributes
            for line in file:
                [attr, vals] = [x.strip() for x in line.split(":")]
                vals = [x.strip() for x in vals.split(",")]
                self.valuesOfAttr[attr] = vals
        self.numberOfAttr = len(self.valuesOfAttr.keys())
        self.attributes = list(self.valuesOfAttr.keys())
        with open(self.dataPath, "r") as file:
            for line in file:
                row = [x.strip() for x in line.split(",")]
                if row != [] or row != [""]:
                    self.data.append(row)

    def preprocessData(self):
        for index, row in enumerate(self.data):
            for attribute_index in range(self.numberOfAttr):
                if(not self.isAttributeDiscrete(self.attributes[attribute_index])):
                    self.data[index][attribute_index] = float(self.data[index][attribute_index])

    def printTree(self):
        self.printNodeDetails(self.tree)

    def printNodeDetails(self, node, indent=""):
        if not node.isLeaf:
            if node.threshold is None:
                #discrete
                for index,child in enumerate(node.children):
                    if child.isLeaf:
                        print(indent + node.label + " = " + self.attributes[index] + " : " + child.label)
                    else:
                        print(indent + node.label + " = " + self.attributes[index] + " : ")
                        self.printNodeDetails(child, indent + "    ")
            else:
                #numerical
                left_child = node.children[0]
                right_child = node.children[1]
                if left_child.isLeaf:
                    print(indent + node.label + " <= " + str(node.threshold) + " : " + left_child.label)
                else:
                    print(indent + node.label + " <= " + str(node.threshold)+" : ")
                    self.printNodeDetails(left_child, indent + "    ")

                if right_child.isLeaf:
                    print(indent + node.label + " > " + str(node.threshold) + " : " + right_child.label)
                else:
                    print(indent + node.label + " > " + str(node.threshold) + " : ")
                    self.printNodeDetails(right_child, indent + "    ")


    def createTree(self):
        self.tree = self.createTreeRecursively(self.data, self.attributes)
        
    def createTreeRecursively(self, currentData, currentAttr):
        isAllIdentical = self.IsAllIdenticalClass(currentData)

        if len(currentData) == 0:
            #Fail
            return Node(True, "Fail", None)
        elif isAllIdentical is not False:
            #return a node with that class
            return Node(True, isAllIdentical, None)
        elif len(currentAttr) == 0:
            #return a node with the majority class
            majorityClass = self.getMajorityClass(currentData)
            return Node(True, majorityClass, None)
        else:
            (best,bestThreshold,splitted) = self.splitAttr(currentData, currentAttr)
            remainAttr = currentAttr[:]
            remainAttr.remove(best)
            node = Node(False, best, bestThreshold)
            node.children = [self.createTreeRecursively(set, remainAttr) for set in splitted]
            return node

    def getMajorityClass(self, currentData):
        frequency = [0]*len(self.classes)
        for row in currentData:
            index = self.classes.index(row[-1])
            frequency[index] += 1
        maximumIndex = frequency.index(max(frequency))
        return self.classes[maximumIndex]


    def IsAllIdenticalClass(self, data):
        for row in data:
            if row[-1] != data[0][-1]:
                return False
        return data[0][-1]

    def isAttributeDiscrete(self, attr):
        if attr not in self.attributes:
            raise ValueError("Attribute not found")
        elif len(self.valuesOfAttr[attr]) == 1 and self.valuesOfAttr[attr][0] == "continuous":
            return False
        else:
            return True

    def splitAttr(self, currentData, currentAttributes):
        splitted = []
        max_Entropy = -1*float("inf")
        bestAttr = -1
        #None for discrete attributes, threshold value for continuous attributes
        bestThreshold = None
        for attribute in currentAttributes:
            indexOfAttribute = self.attributes.index(attribute)
            if self.isAttributeDiscrete(attribute):
                #split curData into n-subsets, where n is the number of 
                #different values of attribute i. Choose the attribute with
                #the max gain
                valuesForAttribute = self.valuesOfAttr[attribute]
                subset = [[] for a in valuesForAttribute]
                for row in currentData:
                    for index in range(len(valuesForAttribute)):
                        if row[i] == valuesForAttribute[index]:
                            subset[index].append(row)
                            break
                e = gain(currentData, subset)
                if e > max_Entropy:
                    max_Entropy = e
                    splitted = subset
                    bestAttr = attribute
                    bestThreshold = None
            else:
                #sort the data according to the column.Then try all 
                #possible adjacent pairs. Choose the one that 
                #yields maximum gain
                currentData.sort(key = lambda x: x[indexOfAttribute])
                for j in range(0, len(currentData) - 1):
                    if currentData[j][indexOfAttribute] != currentData[j + 1][indexOfAttribute]:
                        threshold = (currentData[j][indexOfAttribute] + currentData[j + 1][indexOfAttribute]) / 2
                        less = []
                        greater = []
                        for row in currentData:
                            if(row[indexOfAttribute] > threshold):
                                greater.append(row)
                            else:
                                less.append(row)
                        e = self.info_gain(currentData, [less, greater])
                        if e >= max_Entropy:
                            splitted = [less, greater]
                            max_Entropy = e
                            bestAttr = attribute
                            bestThreshold = threshold
        return (bestAttr,bestThreshold,splitted)

    def info_gain(self, set, subset):
        #input : data and disjoint subsets of it
        #output : information gain
        St = len(set)
        #calculate impurity before split
        impurityBeforeSplit = self.entropy(set)
        #calculate impurity after split
        weights = [len(subset) / St for subset in subset]
        impurityAfterSplit = 0
        for i in range(len(subset)):
            impurityAfterSplit += weights[i]*self.entropy(subset[i])
        #calculate total gain
        totalGain = impurityBeforeSplit - impurityAfterSplit
        return totalGain

    def entropy(self, data):
        S = len(data)
        if S == 0:
            return 0
        numClasses = [0 for i in self.classes]
        for row in data:
            classIndex = list(self.classes).index(row[-1])
            numClasses[classIndex] += 1
        numClasses = [x/S for x in numClasses]
        entropy = 0
        for num in numClasses:
            entropy += num*self.logarithm(num)
        return entropy*-1


    def logarithm(self, x):
        if x == 0:
            return 0
        else:
            return math.log(x,2)
            
    def get_index(self, label):
        for i in range(0, 4):
            if self.attributes[i] == label:
                return i;
        
    def predict(self, values):
        return self.predictRecursive(self.tree, values)
        
    def predictRecursive(self, node, values):
        if not node.isLeaf:
            if node.threshold is None:
                #discrete
                for index,child in enumerate(node.children):
                    if child.isLeaf:
                        return child.label
                    else:
                        return self.predictRecursive(child, values)
            else:
                #numerical
                left_child = node.children[0]
                right_child = node.children[1]
                if left_child.isLeaf:
                    if values[self.get_index(node.label)] <= node.threshold:
                        return left_child.label
                else:
                    return self.predictRecursive(left_child, values)

                if right_child.isLeaf:
                    if values[self.get_index(node.label)] > node.threshold:
                        return right_child.label
                else:
                    return self.predictRecursive(right_child, values)
        
    def calc_accuracy(self, testData):
        rx, cx = testData.shape
        count = 0
        for i in range(0, rx):
            actual = testData[i][4]
            predicted = self.predict([testData[i][0], testData[i][1], testData[i][2], testData[i][3]])
            if(actual == predicted):
                count += 1
        accuracy = count/ rx;
        return accuracy*100
        
        
class Node:
    def __init__(self, isLeaf, label, threshold):
        self.label = label
        self.threshold = threshold
        self.isLeaf = isLeaf
        self.children = []