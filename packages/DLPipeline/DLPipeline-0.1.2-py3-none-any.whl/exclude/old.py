#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'

learning_rate = 3e-5
epochs = 7
cifar10_dataset_folder_path = '/home/heider/Datasets/Classification/cifar/cifar-10-batches-py/'
save_model_path = '/home/heider/Models/DLPipeline/'
batch_size = 64
n_samples = 10
top_n_predictions = 5
cifar_height = 32
cifar_width = 32
image_dims = (224, 224, 3)
label_dims = (10,)
checkpoint_interval = 5
verbosity_level = 1
preprocessed_data_valid_path = 'preprocess_validation.p'
preprocessed_test_data_path = 'preprocess_testing.p'
preprocessed_data_base = '/home/heider/Datasets/Classification/cifar/preprocessed/'
tensorboard_log_path = '/home/heider/tensorboard_logs'
