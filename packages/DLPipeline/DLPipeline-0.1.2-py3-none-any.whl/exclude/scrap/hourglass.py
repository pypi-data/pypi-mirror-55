import tensorflow as tf


def hourglass(input_size, n_features, n_filters, kernel_sizes, mode='PREDICT'):
  conv_kwargs = {
    'strides':   (2, 2),
    'padding':   'same',
    'activation':tf.nn.leaky_relu,
    'use_bias':  True
    }

  print("*** Network mode: " + mode)
  nml_training = (True if mode == 'TRAIN' else False)  # Update batch normalization parameters or use learned?

  features = tf.placeholder(tf.float32, shape=[None, input_size, input_size, 3], name='features')
  labels = tf.placeholder(tf.float32, shape=[None, input_size, input_size, n_features], name='labels')

  # Encoder 1
  layer = tf.layers.batch_normalization(features, training=nml_training, name="Input1BN")
  layers = [layer]
  for i, nf in enumerate(n_filters):
    shape = (kernel_sizes[i], kernel_sizes[i])
    layer = tf.layers.conv2d(layers[-1], nf, shape, name=f"Encoder1Conv{str(i)}", **conv_kwargs)
    layers.append(layer)
    layer = tf.layers.batch_normalization(layers[-1], training=nml_training, name="Encoder1BN" + str(i))
    layers.append(layer)
  # Decoder 1
  for i, nf in enumerate(n_filters[::-1]):
    shape = (kernel_sizes[::-1][i], kernel_sizes[::-1][i])
    lastlayer = (i == len(n_filters) - 1)
    if lastlayer:
      nf = n_features
    layer = tf.layers.conv2d_transpose(layers[-1], nf, shape, name=f"Decoder1Conv{str(i)}", **conv_kwargs)
    layers.append(layer)
    if not lastlayer:
      layer = tf.layers.batch_normalization(layers[-1], training=nml_training, name="Decoder1BN" + str(i))
      layers.append(layer)
  predictions1 = layers[-1]

  layer = tf.layers.batch_normalization(layers[-1], training=nml_training, name="Input2BN")
  layers.append(layer)

  # Encoder 2
  for i, nf in enumerate(n_filters):
    shape = (kernel_sizes[i], kernel_sizes[i])
    layer = tf.layers.conv2d(layers[-1], nf, shape, name=f"Encoder2Conv{str(i)}", **conv_kwargs)
    layers.append(layer)
    layer = tf.layers.batch_normalization(layers[-1], training=nml_training, name="Encoder2BN" + str(i))
    layers.append(layer)
  # Decoder 2
  for i, nf in enumerate(n_filters[::-1]):
    shape = (kernel_sizes[::-1][i], kernel_sizes[::-1][i])
    lastlayer = (i == len(n_filters) - 1)
    if lastlayer:
      nf = n_features
    layer = tf.layers.conv2d_transpose(layers[-1], nf, shape, name=f"Decoder2Conv{str(i)}", **conv_kwargs)
    layers.append(layer)
    if not lastlayer:
      layer = tf.layers.batch_normalization(layers[-1], training=nml_training, name=f"Decoder2BN{str(i)}")
      layers.append(layer)
  predictions2 = layers[-1]

  # Loss
  loss1 = tf.losses.mean_squared_error(labels, predictions1)
  loss2 = tf.losses.mean_squared_error(labels, predictions2)

  return {
    'features':    features,
    'labels':      labels,
    'loss1':       loss1,
    'loss2':       loss2,
    'predictions1':predictions1,
    'predictions2':predictions2
    }
