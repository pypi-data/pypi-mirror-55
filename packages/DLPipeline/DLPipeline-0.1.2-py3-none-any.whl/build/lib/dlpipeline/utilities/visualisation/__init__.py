#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

from matplotlib import pyplot
import numpy
import tqdm
from sklearn.preprocessing import LabelBinarizer

from dlpipeline.utilities.transformation.images import load_label_names


def display_image_predictions(features, labels, predictions):
  n_classes = 10
  label_names = load_label_names()
  label_binariser = LabelBinarizer()
  label_binariser.fit(range(n_classes))
  label_ids = label_binariser.inverse_transform(numpy.array(labels))

  fig, axs = pyplot.subplots(10, 2, figsize=(12, 24))

  margin = 0.05
  ind = numpy.arange(n_classes)
  width = (1. - 2. * margin) / n_classes

  for image_i, (feature, label_id, prediction) in tqdm.tqdm(enumerate(zip(features, label_ids, predictions))):
    correct_name = label_names[label_id]
    pred_name = label_names[numpy.argmax(prediction)]

    is_match = 'False'

    if numpy.argmax(prediction) == label_id:
      is_match = 'True'

    predictions_array = []
    pred_names = []

    for index, pred_value in tqdm.tqdm(enumerate(prediction)):
      tmp_pred_name = label_names[index]
      predictions_array.append({tmp_pred_name:pred_value})
      pred_names.append(tmp_pred_name)

    print(
        '[{}] ground truth: {}, predicted result: {} | {}'.format(image_i, correct_name, pred_name, is_match))
    print('\t- {}\n'.format(predictions_array))

    #         print('image_i: ', image_i)
    #         print('axs: ', axs, ', axs len: ', len(axs))
    axs[image_i][0].imshow(feature)
    axs[image_i][0].set_title(pred_name)
    axs[image_i][0].set_axis_off()

    axs[image_i][1].barh(ind + margin, prediction, width)
    axs[image_i][1].set_yticks(ind + margin)
    axs[image_i][1].set_yticklabels(pred_names)

  pyplot.tight_layout()
