#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tensorflow.keras.datasets import fashion_mnist

__author__ = 'Christian Heider Nielsen'

from matplotlib import pyplot
import tensorflow as tf
from tensorflow import keras

import dlpipeline
from dlpipeline.utilities.visualisation.plot_image import plot_image
from dlpipeline.utilities.visualisation.plot_value_array import plot_value_array


def main() -> None:
  (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

  class_names = ['T - shirt / top',
                 'Trouser',
                 'Pullover',
                 'Dress',
                 'Coat',
                 'Sandal',
                 'Shirt',
                 'Sneaker',
                 'Bag',
                 'Ankle boot']

  pyplot.figure()
  pyplot.imshow(train_images[0])
  pyplot.colorbar()
  pyplot.grid(False)
  pyplot.show()

  train_images = train_images / 255.0

  test_images = test_images / 255.0

  pyplot.figure(figsize=(10, 10))
  for i in range(25):
    pyplot.subplot(5, 5, i + 1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.grid(False)
    pyplot.imshow(train_images[i], cmap=pyplot.cm.binary)
    pyplot.xlabel(class_names[train_labels[i]])
  pyplot.show()

  model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

  model.compile(optimizer=tf.train.AdamOptimizer(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

  model.fit(train_images, train_labels, epochs=5)

  test_loss, test_acc = model.evaluate(test_images, test_labels)

  print('Test accuracy:', test_acc)

  predictions = model.predict(test_images)

  i = 0
  pyplot.figure(figsize=(6, 3))
  pyplot.subplot(1, 2, 1)
  dlpipeline.utilities.visualisation.plot_image.plot_image(i, predictions, test_labels, test_images,
                                                           class_names)
  pyplot.subplot(1, 2, 2)
  dlpipeline.utilities.visualisation.plot_value_array.plot_value_array(i, predictions, test_labels,
                                                                       class_names)
  pyplot.show()

  i = 12
  pyplot.figure(figsize=(6, 3))
  pyplot.subplot(1, 2, 1)
  plot_image(i, predictions, test_labels, test_images, class_names)
  pyplot.subplot(1, 2, 2)
  plot_value_array(i, predictions, test_labels, class_names)
  pyplot.show()
  # Plot the first X test images, their predicted label, and the true label
  # Color correct predictions in blue, incorrect predictions in red

  num_rows = 5
  num_cols = 3
  num_images = num_rows * num_cols
  pyplot.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
  for i in range(num_images):
    pyplot.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions, test_labels, test_images, class_names)
    pyplot.subplot(num_rows, 2 * num_cols, 2 * i + 2)
    plot_value_array(i, predictions, test_labels, class_names, show_ticks=False)
  pyplot.show()


'''
  # Grab an image from the test dataset
  img = test_images[0]

  # Add the image to a batch where it's the only member.
  img = (numpy.expand_dims(img, 0))

  predictions_single = model.predict(img)

  plot_value_array(0, predictions_single, test_labels, class_names)
'''

if __name__ == '__main__':
  main()
