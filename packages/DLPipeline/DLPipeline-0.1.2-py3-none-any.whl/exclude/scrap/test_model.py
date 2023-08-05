#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from dlpipeline.classifier.tf_classifier import TFClassifier

__author__ = 'Christian Heider Nielsen'

import dlpipeline.utilities.configurations.base_config as C
from samples.demo.load import (load_graph,
                               load_labels,
                               image_to_tensor,
                               )


def parse_arguments(C):
  '''
  for mobilenet

  python label_image.py \
--graph=/tmp/output_graph.pb \
--labels=/tmp/output_labels.txt \
--input_layer=Placeholder \
--output_layer=final_result \
--input_height=224 \
--input_width=224 \
--image=$HOME/flower_photos/daisy/21652746_cc379e0eea_m.jpg

  '''

  file_name = "/home/captain/Pictures/download.jpeg"
  model_file = "/home/captain/Projects/IBBD5/dlpipeline/exclude/inception_v3_2016_08_28_frozen.pb"
  label_file = "/home/captain/Projects/IBBD5/dlpipeline/exclude/imagenet_slim_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255
  input_layer_name = "input"
  output_layer_name = "InceptionV3/Predictions/Reshape_1"

  parser = argparse.ArgumentParser()
  parser.add_argument("--file_name", help="image to be processed", default=file_name)
  parser.add_argument("--model_file", help="graph/model to be executed", default=model_file)
  parser.add_argument("--label_file", help="name of file containing labels", default=label_file)
  parser.add_argument("--input_height", type=int, help="input height", default=input_height)
  parser.add_argument("--input_width", type=int, help="input width", default=input_width)
  parser.add_argument("--input_mean", type=int, help="input mean", default=input_mean)
  parser.add_argument("--input_std", type=int, help="input std", default=input_std)
  parser.add_argument("--input_layer_name", help="name of input layer", default=input_layer_name)
  parser.add_argument("--output_layer_name", help="name of output layer", default=output_layer_name)
  args = parser.parse_args()
  return args


def test_model():
  args = parse_arguments(C)

  args.file_name = '/home/captain/Pictures/456477.jpg'
  args.model_file = '/home/captain/Projects/IBBD5/Models/RetinaLyze/1540479815.9992564/output_graph'
  args.label_file = '/home/captain/Projects/IBBD5/Models/RetinaLyze/1540479815.9992564/output_labels.txt'
  args.input_layer_name = 'jpeg_str_placeholder'
  args.output_layer_name = 'softmax_output'

  model_graph = load_graph(args.model_file)
  input_tensor = image_to_tensor(args.file_name,
                                 input_height=args.input_height,
                                 input_width=args.input_width,
                                 input_mean=args.input_mean,
                                 input_std=args.input_std)

  tfc = TFClassifier()
  results = tfc.predict(model_graph, input_tensor, **vars(args))

  k = 5
  top_k = results.argsort()[-k:][::-1]
  labels = load_labels(args.label_file)

  for i in top_k:
    print(labels[i], results[i])


if __name__ == "__main__":

  test_model()
