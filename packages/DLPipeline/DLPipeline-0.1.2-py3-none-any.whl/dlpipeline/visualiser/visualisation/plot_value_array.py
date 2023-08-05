#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

from matplotlib import pyplot
import numpy


def plot_value_array(i, predictions_array, true_label, class_names, show_ticks=True, size=8, rotation=90):
  predictions_array, true_label = predictions_array[i], true_label[i]
  pyplot.grid(False)
  pyplot.xticks([])
  pyplot.yticks([])
  this_plot = pyplot.bar(range(10), predictions_array, color="#777777")
  pyplot.ylim([0, 1])
  predicted_label = numpy.argmax(predictions_array)

  this_plot[predicted_label].set_color('red')
  this_plot[true_label].set_color('blue')
  if show_ticks:
    _ = pyplot.xticks(range(len(class_names)), class_names, rotation=rotation, fontsize=size)
    # pyplot.tick_params(axis='both', which='minor', labelsize=size)
    # plot.tick_params(axis='both', which='major', labelsize=size*1.2)
