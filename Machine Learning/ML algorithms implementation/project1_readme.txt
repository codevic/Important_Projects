
lin_regression.txt contains the linear regression matlab codes

------------------------------------------------------------------
In ATNT50 directory we have

trainDataXY.txt   

It contains 45 images. image 1-9 from class 1. image 10-18 from class 2. etc.
Each image is a column. 1st row are class labels.

testDataXY.txt     

It contain 5 images. 
Each image is a column. 1st row are class labels.

------------------------------------------------------------------------------------
You train the classifer using training data. Once classifier is trained,
you classifer the data in testData, and compare the obtained class labels 
to the groud-truth label provided there. 

These two data are simple training and testing data.
They are warm-up data, so you can see how your classifer work on this simple data. 

-------------------------------------------------------------------------------------


data set: ATNT-face-image400.txt  :

Text file. 
1st row is cluster labels. 
2nd-end rows: each colum is a feature vectors (vector length=28x23).

Total 40 classes. each class has 10 images. Total 40*10=400 images

----------------------------------------------------------------------------------------

data set: Hand-written-26-letters.txt :

Text file. 
1st row is cluster labels. 
2nd-end rows: each colum is a feature vectors (vector length=20x16).

Total 26 classes. each class has 39 images. Total 26*39=1014 images.


-------------------------------------------------------------------------------------
Once you are confident that your classifer works correctly,
you are to use 5-fold cross-validation (CV) assess/evaluate the classifer.
You do CV using the following two full datasets.

ATNT face images data are generally easier, i.e., you get high classification accuracy.

You run classifier on ATNT data first, to make sure you get correct results.

Hand-written-letters data are harder to classify, i.e., you get lower classification accuracy.

You run classifier on hand-written-letter data only after you are confident 
that your classifier works correctly.

Your tasks:

(A)
On ATNT data, 
run 5-fold cross-validation using  each of the four classifers:
KNN, centroid, linear regression and SVM.
Report the classification accuracy on each classifier.
Remember, each of the 5-fold CV gives one accuracy. You need to present all 5 accuracy numbers
for each classifier.


(B£©
On the hand-written-letter data,
repeat the above 5-fold CV using the four classifers.

(C)
You should have the ability to generate a training data and test data
from the ATNT or hand-written-letter data.

For example, from ATNT data, generate a training data using the first 9 images of a class 
and the test data using the remaining 1 image of the class. Thus the training data contains 
9*40=360 images and the list of corresponding class labels. The test data contains 1*40=40 images
and the list of corresponding class labels.
(The data in ATNT50 are generated in this way)

Another example. Generate a 2-class data for the 2-class SVM classifier.
For example, pick "C" and "F" classes from the hand-written-letter data. Using the first 30 images
in "C" and in "F" to form the training data. Using the remaining 9 images in each class to form the 
test data.

-------------------------------------------------------------------------------
The quiz or exam will ask you to do something very similar to tasks A, B, C.
-------------------------------------------------------------------------------



