#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import albumentations as A
from matplotlib import pyplot

from dlpipeline.augmentor.dlp_augmentor import DLPAugmentor
from dlpipeline.visualiser.visualisation.bbox import augment_and_show, decode_image, visualise

__author__ = 'Christian Heider Nielsen'


class AlbumentationsAugmentor(DLPAugmentor):
  def pipeline_function(self, arg_data, **kwargs) -> dict:
    data = self.augment(arg_data)
    return {'data':data}

  def __init__(self, C=None, aug_fn=None, p=.7, **kwargs):
    super().__init__(C=C, **kwargs)

    self._aug_fn = aug_fn
    if not self._aug_fn:
      self._aug_fn = get_strong_aug(p)

  def augment(self, images):
    if isinstance(images, tuple):
      return [self._aug_fn(image=image)['image'] for image in images]
    return self._aug_fn(image=images)['image']

  def augment_and_display(self, image, title=''):
    r = self._aug_fn(image=image)
    image = r['image']
    pyplot.figure(figsize=(10, 10))
    pyplot.title(title)
    pyplot.imshow(image)
    pyplot.show()


def get_bbox_aug(aug,
                 min_area=0.,
                 min_visibility=0.):
  return A.Compose(aug, bbox_params={'format':        'coco',
                                     'min_area':      min_area,
                                     'min_visibility':min_visibility,
                                     'label_fields':  ['category_id']
                                     })


def get_strong_aug(p):
  return A.Compose([
    A.Rotate(45, p=p),
    A.Flip(),
    A.Transpose(),
    A.OneOf([
      A.IAAAdditiveGaussianNoise(),
      A.GaussNoise(),
      ], p=0.2),
    A.OneOf([
      A.MotionBlur(p=.2),
      A.MedianBlur(blur_limit=3, p=.1),
      A.Blur(blur_limit=3, p=.1),
      ], p=0.2),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=32, p=0.8),
    A.OneOf([
      A.OpticalDistortion(p=0.3),
      A.GridDistortion(p=.1),
      A.IAAPiecewiseAffine(p=0.3),
      ], p=0.2),
    A.OneOf([
      # A.CLAHE(clip_limit=2),
      A.IAASharpen(),
      A.IAAEmboss(),
      A.RandomBrightnessContrast(),
      ], p=0.3),
    A.HueSaturationValue(p=0.3),
    ], p=p)


def main():
  augmentor = AlbumentationsAugmentor([image])

  augment_and_show(augmentor._aug_fn, image)

  annotations = {'image':      image,
                 'bboxes':     [[366.7,
                                 80.84,
                                 132.8,
                                 181.84],
                                [5.66,
                                 138.95,
                                 147.09,
                                 164.88]],
                 'category_id':[18, 17]
                 }
  category_id_to_name = {17:'cat',
                         18:'dog'
                         }

  augmented = get_bbox_aug([A.VerticalFlip(p=1.),
                            A.HorizontalFlip(p=1.)])(**annotations)
  visualise(augmented['image'], augmented['bboxes'], augmented['category_id'], category_id_to_name)


def main2(images):
  augmentor = AlbumentationsAugmentor()

  aug_im = augmentor.augment(image)
  visualise(aug_im)


if __name__ == '__main__':
  path__ = '/home/heider/Pictures/Screenshot_2018-12-04_16-50-53.png'

  with open(path__, 'rb') as f:
    image = decode_image(f.read())

  main2(image)
