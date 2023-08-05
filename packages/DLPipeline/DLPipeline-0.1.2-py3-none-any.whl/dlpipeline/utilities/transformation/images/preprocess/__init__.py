#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

import pickle

import numpy


def load_cfar10_batch(cifar10_dataset_folder_path, batch_id):
  with open(cifar10_dataset_folder_path + '/data_batch_' + str(batch_id), mode='rb') as file:
    # note the encoding type is 'latin1'
    batch = pickle.load(file, encoding='latin1')

  features = batch['data'].reshape((len(batch['data']), 3, 32, 32)).transpose(0, 2, 3, 1)
  labels = batch['labels']

  return features, labels


def _preprocess_and_save(one_hot_encode, features, labels, filename):
  labels = one_hot_encode(labels)

  pickle.dump((features, labels), open(filename, 'wb'))


def preprocess_and_save_data(cifar10_dataset_folder_path, one_hot_encode):
  n_batches = 5
  valid_features = []
  valid_labels = []

  for batch_i in range(1, n_batches + 1):
    features, labels = load_cfar10_batch(cifar10_dataset_folder_path, batch_i)

    # find index to be the point as validation data in the whole dataset of the batch (10%)
    index_of_validation = int(len(features) * 0.1)

    # preprocess the 90% of the whole dataset of the batch
    # - normalize the features
    # - one_hot_encode the lables
    # - save in a new file named, "preprocess_batch_" + batch_number
    # - each file for each batch
    _preprocess_and_save(one_hot_encode,
                         features[:-index_of_validation], labels[:-index_of_validation],
                         'preprocess_batch_' + str(batch_i) + '.p')

    # unlike the training dataset, validation dataset will be added through all batch dataset
    # - take 10% of the whold dataset of the batch
    # - add them into a list of
    #   - valid_features
    #   - valid_labels
    valid_features.extend(features[-index_of_validation:])
    valid_labels.extend(labels[-index_of_validation:])

  # preprocess the all stacked validation dataset
  _preprocess_and_save(one_hot_encode,
                       numpy.array(valid_features), numpy.array(valid_labels),
                       'preprocess_validation.p')

  # load the test dataset
  with open(cifar10_dataset_folder_path + '/test_batch', mode='rb') as file:
    batch = pickle.load(file, encoding='latin1')

  # preprocess the testing data
  test_features = batch['data'].reshape((len(batch['data']), 3, 32, 32)).transpose(0, 2, 3, 1)
  test_labels = batch['labels']

  # Preprocess and Save all testing data
  _preprocess_and_save(one_hot_encode,
                       numpy.array(test_features), numpy.array(test_labels),
                       'preprocess_testing.p')
