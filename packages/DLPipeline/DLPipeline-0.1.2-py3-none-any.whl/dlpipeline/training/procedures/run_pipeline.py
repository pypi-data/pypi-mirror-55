# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

from tensorflow._api.v2.compat.v1 import train
from tensorflow.python import (Session,
                               get_default_graph,
                               global_variables_initializer,
                               group,
                               logging,
                               reset_default_graph,
                               tables_initializer,
                               )
from tensorflow.python.summary import summary

from dlpipeline import TFAugmentor, TFDataLoader
from dlpipeline.classifier.tf_classifier import TFClassifier
from dlpipeline.embedder.tf_hub_embedder import TFHubEmbedder
from dlpipeline.utilities.hub_size import get_hub_sizes
from dlpipeline.visualiser.visualisation.confusion_matrix import plot_confusion_matrix
from samples.demo.web_app_demo.app import create_app


def run_pipeline(*,
                 tf_config,
                 default_do_augmentation,
                 fine_tune_embedder,
                 summaries_directory: Path,
                 train_batch_size,
                 begin_augmenting_at_step,
                 eval_step_interval,
                 steps,
                 logging_interval,
                 intermediate_store_frequency,
                 checkpoint_name,
                 intermediate_output_graphs_directory,
                 output_labels_file_name,
                 data_loader_type=TFDataLoader,
                 augmentor_type=TFAugmentor,
                 embedder_type=TFHubEmbedder,
                 model_type=TFClassifier,

                 **kwargs
                 ):
  '''pipeline=(TFDataLoader,
            AlbumentationsAugmentor,
            TFHubEmbedder,
            TFClassifier),
  '''

  reset_default_graph()
  graph = get_default_graph()
  with graph.as_default() as graph:
    with Session(config=tf_config, graph=graph) as sess:

      # region Pipeline Setup

      data_loader = data_loader_type(C=kwargs)
      if augmentor_type:
        augmentor = augmentor_type(C=kwargs, default_do_augmentation=default_do_augmentation)
      else:
        augmentor = None

      embedder = embedder_type(C=kwargs,
                               cache_embeddings=default_do_augmentation,
                               fine_tune_embedder=fine_tune_embedder)

      model = model_type(C=kwargs,
                         input_size=embedder.embedding_size,
                         output_size=data_loader.class_count,
                         additional_evaluation_terms=(embedder.embedder_loss,))

      # endregion

      # region Building

      sizes = get_hub_sizes(kwargs)

      data_loader.build(**sizes, sess=sess)
      pipeline = (augmentor,
                  embedder,
                  model)

      for module in pipeline:
        if module:
          module.build(**sizes, sess=sess)

      init_op = group([global_variables_initializer(), tables_initializer()])
      sess.run(init_op)

      train_saver = train.Saver()

      logging.set_verbosity(logging.INFO)

      train_writer = summary.FileWriter(summaries_directory / 'training_set', sess.graph)
      validation_writer = summary.FileWriter(summaries_directory / 'validation_set')

      # endregion

      val_gen = data_loader.sampler(set_name='validation', sess=sess)

      step_i = 0
      for batch in data_loader.sampler(set_name='training', batch_size=train_batch_size, sess=sess):

        ret = None
        x = batch['data']
        for module in pipeline:
          if module:
            ret = module.apply(x, sess=sess, **batch)

            if 'data' in ret:
              x = ret['data']

        step_i += 1
        if hasattr(ret, 'train_summary'):
          train_writer.add_summary(ret['train_summary'], step_i)

        # region Switches

        if step_i == begin_augmenting_at_step:
          if augmentor_type:
            augmentor.do_augment = True
          embedder.do_cache_embeddings = False
          print('Started data augmention')

        # endregion

        # region Validation

        if (step_i % eval_step_interval) == 0 or step_i + 1 == steps:
          (train_accuracy,
           cross_entropy_value,
           cf_mat_value) = sess.run([model.evaluation['accuracy'],
                                     model.classifier['cross_entropy_node'],
                                     model.evaluation['cf_mat']],
                                    feed_dict={
                                        model.classifier['input_node']:x,
                                        model.classifier['label_node']:batch['label_index']
                                        }
                                    )

          conf_mat = plot_confusion_matrix(labels=data_loader.keys(),
                                           tensor_name='training/confusion_matrix',
                                           title="Confusion Matrix (Training)",
                                           conf_mat=cf_mat_value)
          train_writer.add_summary(conf_mat, step_i)

          v = val_gen.__next__()
          v_embedding = embedder.apply(v['data'],
                                       label_index=v['label_index'],
                                       label_name=v['label_name'],
                                       data_path=v['data_path'],
                                       sess=sess)

          (validation_summary,
           validation_accuracy,
           validation_cf_mat_value) = sess.run([model.summary,
                                                model.evaluation['accuracy'],
                                                model.evaluation['cf_mat']],
                                               feed_dict={
                                                   model.classifier['input_node']:v_embedding['data'],
                                                   model.classifier['label_node']:v['label_index']
                                                   }
                                               )

          validation_writer.add_summary(validation_summary, step_i)

          val_conf_mat = plot_confusion_matrix(labels=data_loader.keys(),
                                               tensor_name='validation/confusion_matrix',
                                               title="Confusion Matrix (Validation)",
                                               conf_mat=validation_cf_mat_value)
          validation_writer.add_summary(val_conf_mat, step_i)

          if step_i % logging_interval == 0:
            logging.info(f'{datetime.now()}: '
                         f'Step {step_i:d}: '
                         f'Train accuracy = {train_accuracy * 100:.1f}%%')
            logging.info(f'{datetime.now()}: '
                         f'Step {step_i:d}: '
                         f'Cross entropy = {cross_entropy_value:f}')
            logging.info(f'{datetime.now()}: '
                         f'Step {step_i:d}: '
                         f'Validation accuracy = {validation_accuracy * 100:.1f}%% '
                         f'(N={len(v["label_index"]):d})')

        # endregion

        # region Checkpointing

        if (intermediate_store_frequency and
            (step_i % intermediate_store_frequency == 0) and
            step_i > 0):
          model.intermediate_save(step_i,
                                  data_loader.class_count,
                                  train_saver,
                                  checkpoint_name=checkpoint_name + str(step_i),
                                  intermediate_output_graphs_directory=intermediate_output_graphs_directory,
                                  module_specification=embedder.module_specification)

        # endregion

        # region Stopping

        if step_i > steps:
          break

        # endregion

      # region Saving

      train_saver.save(sess, checkpoint_name + str(step_i))

      saved_model_path = model.save(data_loader,
                                    checkpoint_name + str(step_i),
                                    kwargs,
                                    embedder.module_specification)

      model.test(sess,
                 data_loader,
                 kwargs,
                 embedder=embedder,
                 graph_handles={'resized_image_node':  data_loader._handles['resized_image_node'],
                                'jpeg_str_placeholder':data_loader._handles['jpeg_str_placeholder']
                                })

      # endregion

      # region Webapp

      print('Finished')
      print('Launching web app')

      app = create_app(base_path=saved_model_path, labels_path=output_labels_file_name)
      app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

      # endregion


if __name__ == '__main__':
  run_pipeline()
