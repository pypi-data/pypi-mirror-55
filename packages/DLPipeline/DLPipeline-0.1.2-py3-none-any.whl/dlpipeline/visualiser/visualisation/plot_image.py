#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

from matplotlib import pyplot
import numpy


def plot_image(i, predictions_array, true_label, img, class_names):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  pyplot.grid(False)
  pyplot.xticks([])
  pyplot.yticks([])

  pyplot.imshow(img, cmap=pyplot.cm.binary)

  predicted_label = numpy.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  pyplot.xlabel(
      f"{class_names[predicted_label]} {100 * numpy.max(predictions_array):2.0f}% ({class_names[true_label]})",
      color=color)
