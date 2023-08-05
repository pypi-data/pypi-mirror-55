#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dlpipeline.visualiser.tf_visualiser import TFVisualiser

__author__ = 'Christian Heider Nielsen'

import tensorflow as tf


def classification_net(*,
                       input_size,
                       output_size,
                       is_training,
                       batch_size=None,
                       learning_rate=0,
                       quantize=False,
                       stddev=0.001,
                       hidden_layers=(64, 32),
                       visualiser=TFVisualiser(),
                       additional_evaluation_terms=(),
                       **kwargs):
  '''
  Adds a new softmax and fully-connected layer for training and eval.

  We need to retrain the top layer to identify our new classes, so this function
  adds the right operations to the graph, along with some variables to hold the
  weights, and then sets up all the gradients for the backward pass.

  The set up for the softmax and fully-connected layers is based on:
  https://www.tensorflow.org/tutorials/mnist/beginners/index.html

  Args:
    class_count: Integer of how many categories of things we're trying to
        recognize.
    final_node_name: Name string for the new final node that produces results.
    embedding_output_node: The output of the main CNN graph.
    quantize_layer: Boolean, specifying whether the newly added layer should be
        instrumented for quantization with TF-Lite.
    is_training: Boolean, specifying whether the newly add layer is for training
        or eval.

  Returns:
    The tensors for the training and cross entropy results, and tensors for the
    embedding input and ground truth input.
    :param visualiser:
    :param embedding_output_node:
    :param output_size:
    :param input_size:
    :param quantize:
    :param is_training:
    :param output_node_name:
    :param learning_rate:
  '''

  assert batch_size is None

  with tf.name_scope('classifier'):
    with tf.name_scope('placeholders'):
      input_node = tf.placeholder(tf.float32,
                                  shape=[batch_size, input_size],
                                  name='features_placeholder'
                                  )

      label_node = tf.placeholder(tf.int64, shape=[batch_size], name='label_placeholder')

      last_layer_node = input_node
      last_layer_size = input_size

    with tf.name_scope(f'layers'):
      for layer_size, i in zip(hidden_layers, range(len(hidden_layers))):

        with tf.name_scope(f'W_{i}'):
          initial_value = tf.truncated_normal([last_layer_size, layer_size], stddev=stddev)
          layer_weights = tf.Variable(initial_value, name='weights')
          visualiser.visualise_variable(layer_weights)

        with tf.name_scope(f'b_{i}'):
          layer_biases_out = tf.Variable(tf.zeros([layer_size]), name='biases')
          visualiser.visualise_variable(layer_biases_out)

        with tf.name_scope(f'Wx_b_{i}'):
          mul = tf.matmul(last_layer_node, layer_weights) + layer_biases_out
          tf.summary.histogram(f'mul', last_layer_node)
          last_layer_node = tf.nn.relu(mul)
          tf.summary.histogram(f'activations', last_layer_node)

        last_layer_size = layer_size

        '''
        hidden_layers2 = [hidden_layer_size//2]
  
        for units in hidden_layers2:
          last_layer_node = tf.layers.dense(last_layer_node, units=units, activation=tf.nn.relu)
  
        last_layer_size = hidden_layer_size//2
        '''

      with tf.name_scope('W_out'):
        initial_value_out = tf.truncated_normal([last_layer_size, output_size], stddev=stddev)
        layer_weights_out = tf.Variable(initial_value_out, name='weights')
        visualiser.visualise_variable(layer_weights_out)

      with tf.name_scope('b_out'):
        layer_biases_out = tf.Variable(tf.zeros([output_size]), name='biases')
        visualiser.visualise_variable(layer_biases_out)

      with tf.name_scope('Wx_b_out'):
        logits = tf.matmul(last_layer_node, layer_weights_out) + layer_biases_out
        tf.summary.histogram('logits', logits)

  prediction_node = tf.nn.softmax(logits, name='softmax_output')
  tf.summary.histogram(f'softmax_output', prediction_node)

  if quantize:
    if is_training:
      tf.quantize.create_training_graph()
    else:
      tf.quantize.create_eval_graph()

  if not is_training:  # If this is an eval graph, we don't need to add loss ops or an optimizer.
    return None, None, input_node, label_node, prediction_node

  with tf.name_scope('cross_entropy_loss'):
    cross_entropy_node = tf.losses.sparse_softmax_cross_entropy(labels=label_node,
                                                                logits=logits)

    tf.summary.scalar('cross_entropy_loss', cross_entropy_node)

  with tf.name_scope('external_addition_terms'):
    add_terms = tf.reduce_sum(additional_evaluation_terms)

  beta = 0.01

  with tf.name_scope('optimiser'):
    # optimiser = tf.train.GradientDescentOptimizer(learning_rate)
    optimiser = tf.train.AdamOptimizer(learning_rate)
    loss = tf.add(cross_entropy_node, add_terms)
    loss = tf.add(loss, beta * tf.nn.l2_loss(layer_weights_out))
    train_step_node = optimiser.minimize(loss)

  return {'train_step_node':   train_step_node,
          'cross_entropy_node':cross_entropy_node,
          'input_node':        input_node,
          'label_node':        label_node,
          'prediction_node':   prediction_node,
          'optimiser':         optimiser
          }
