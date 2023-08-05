#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from experiments.config.base_config import learning_rate

from dlpipeline.utilities.transformation.images import batch_features_labels

__author__ = 'Christian Heider Nielsen'

import tensorflow as tf
import tensornets as nets
import tqdm

# ImageNet input image shape is (244, 244, 3)
inputs = tf.placeholder(tf.float32, [None, 224, 224, 3])

# Output is dependent on your situation (10 for CIFAR-10)
outputs = tf.placeholder(tf.float32, [None, 10])

# VGG19 returns the last layer (softmax)
# model to give the name
logits = nets.VGG19(inputs, is_training=True, classes=10)
model = tf.identity(logits, name='logits')

# loss function applied to the last layer, train on the loss (Adam Optimizer is used)
loss = tf.losses.softmax_cross_entropy(outputs, logits)
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

x = tf.placeholder(tf.float32, shape=(None, 224, 224, 3), name='input_x')
y = tf.placeholder(tf.float32, shape=(None, 10), name='output_y')

# for measuring accuracy after forward passing
correct_pred = tf.equal(tf.argmax(model, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32), name='accuracy')

with tf.Session() as sess:
  # Initializing the variables
  sess.run(tf.global_variables_initializer())

  # Loading the parameters
  sess.run(logits.pretrained())


def training_loop():
  total_valid_acc = 0
  valid_acc = 0

  for batch_valid_images, batch_valid_labels in tqdm.tqdm(batch_features_labels(valid_images,
                                                                                valid_labels,
                                                                                batch_size)
                                                          ):
    valid_acc += sess.run(accuracy, {x:batch_valid_images, y:batch_valid_labels})

  total_num_batch = valid_images.shape[0] / batch_size

  print('Validation Accuracy: {:.6f}'.format(total_valid_acc / total_num_batch))


if __name__ == '__main__':
  training_loop()
