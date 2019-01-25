#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:45:14 2017

@author: qichengwang

Reference: https://www.tensorflow.org/versions/r1.2/get_started/mnist/beginners
"""

""" Installation
https://www.tensorflow.org/install/
"""
import tensorflow as tf

"""The MNIST data is hosted on Yann LeCun's website. 
The MNIST data is split into three parts: 55,000 data points of training data (mnist.train), 
10,000 points of test data (mnist.test), and 5,000 points of validation data (mnist.validation). 
"""
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

"""x isn't a specific value. 
It's a placeholder, a value that we'll input when we ask TensorFlow to run a computation.
Each image is 28 pixels by 28 pixels. 28*28 = 784 
"""
x = tf.placeholder(tf.float32, [None, 784])


W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder(tf.float32, [None, 10])


"""cross-entropy function :−∑y′log⁡(y)"""
"""First, tf.log computes the logarithm of each element of y. 
Next, we multiply each element of y_ with the corresponding element of tf.log(y). 
Then tf.reduce_sum adds the elements in the second dimension of y, due to the reduction_indices=[1] parameter. 
Finally, tf.reduce_mean computes the mean over all the examples in the batch."""
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))


"""In this case, we ask TensorFlow to minimize cross_entropy 
using the gradient descent algorithm with a learning rate of 0.05. """
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy)

  
""" launch the model in an InteractiveSession"""
sess = tf.InteractiveSession()



"""create an operation to initialize the variables we created"""
tf.global_variables_initializer().run()



"""we'll run the training step 1000 times!"""
for _ in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  """print out the result every 100 iterations"""
  if _ % 100 == 0 :
      correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
      accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))     
      print("accuracy:",sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
      print("cross_entropy_train:",sess.run(cross_entropy, feed_dict={x: batch_xs, y_: batch_ys}),end = ",")
      print("cross_entropy_test:",sess.run(cross_entropy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
print("cross_entropy_train:",sess.run(cross_entropy, feed_dict={x: batch_xs, y_: batch_ys}),end = ",")
print("cross_entropy_test:",sess.run(cross_entropy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
