#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

import numpy


def one_hot_encode(x):
  '''
      argument
          - x: a list of labels
      return
          - one hot encoding matrix (number of labels, number of class)
  '''
  encoded = numpy.zeros((len(x), 10))

  for idx, val in enumerate(x):
    encoded[idx][val] = 1

  return encoded
