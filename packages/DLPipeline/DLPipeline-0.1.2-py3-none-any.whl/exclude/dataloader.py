#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

import tensorflow as tf


def load_data(self, filenames=tf.constant(["/var/data/image1.jpg", "/var/data/image2.jpg"]),
              labels=tf.constant(
                  [0, 37])):
  # Reads an image from a file, decodes it into a dense tensor, and resizes it
  # to a fixed shape.
  def _parse_function(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string)
    image_resized = tf.image.resize_images(image_decoded, [28, 28])
    return image_resized, label

  dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
  dataset = dataset.map(_parse_function)
