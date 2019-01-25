#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Created on Tue Oct 31 20:45:14 2017

@author: qichengwang
"""

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf

"""first layer"""
x = tf.placeholder(tf.float32, [None, 784])

W1 = tf.Variable(tf.random_normal([784, 500]))
b1 = tf.Variable(tf.zeros([500]))
z1 = tf.matmul(x, W1) + b1
h1 = tf.nn.relu(z1)

"""second layer"""
W2 = tf.Variable(tf.random_normal([500, 500]))
b2 = tf.Variable(tf.zeros([500]))
z2 = tf.matmul(h1, W2) + b2
h2 = tf.nn.sigmoid(z2)

"""third layer"""
W3 = tf.Variable(tf.random_normal([500, 10]))
b3 = tf.Variable(tf.zeros([10]))
z3 = tf.matmul(h2, W3) + b3

y = z3

y_ = tf.placeholder(tf.float32, [None, 10])

"""Note that in the source code, we don't use this formulation, because it is numerically unstable.
Instead, we apply tf.nn.softmax_cross_entropy_with_logits on the unnormalized logits
(e.g., we call softmax_cross_entropy_with_logits on tf.matmul(x, W) + b),
because this more numerically stable function internally computes the softmax activation.
"""
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

for _ in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    if _ % 100 == 0:
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        print("accuracy:", sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
        print("cross_entropy_train:", sess.run(cross_entropy, feed_dict={x: batch_xs, y_: batch_ys}), end=",")
        print("cross_entropy_test:", sess.run(cross_entropy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))