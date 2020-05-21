# coding=utf-8
# Copyright 2020 The uncertainty_metrics Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Tests for general calibration error.

"""

import itertools

from absl.testing import parameterized
import numpy as np
import tensorflow.compat.v2 as tf
from uncertainty_metrics import general_calibration_error as um


class GeneralCalibrationErrorTest(parameterized.TestCase, tf.test.TestCase):

  def test_consistency(self):
    probs = np.array([[0.42610548, 0.41748077, 0.15641374],
                      [0.44766216, 0.47721294, 0.0751249],
                      [0.1862702, 0.15139402, 0.66233578],
                      [0.05753544, 0.8561222, 0.08634236],
                      [0.18697925, 0.29836466, 0.51465609]])

    labels = np.array([0, 1, 2, 1, 2])
    calibration_error = um.gce(
        probs, labels, num_bins=30, binning_scheme='even',
        class_conditional=False, max_prob=True, norm='l1')
    self.assertAlmostEqual(calibration_error, 0.412713502)

  def test_binary_1d(self):
    probs = np.array([.91, .32, .66, .67, .57, .98, .41, .19])
    labels = np.array([1, 0, 1, 1, 0, 1, 0, 0])
    calibration_error = um.gce(
        probs, labels, num_bins=30, binning_scheme='even',
        class_conditional=False, max_prob=True, norm='l1')
    self.assertAlmostEqual(calibration_error, 0.18124999999999997)

  def test_binary_2d(self):
    probs = np.array(
        [.91, .32, .66, .67, .57, .98, .41, .19]).reshape(8, 1)
    labels = np.array([1, 0, 1, 1, 0, 1, 0, 0])
    calibration_error = um.gce(
        probs, labels, num_bins=30, binning_scheme='even',
        class_conditional=False, max_prob=True, norm='l1')
    self.assertAlmostEqual(calibration_error, 0.18124999999999997)

  def generate_params():  # pylint: disable=no-method-argument
    # 'self' object cannot be passes to parameterized.
    names = ['binning_scheme', 'max_probs', 'class_conditional',
             'threshold', 'norm']
    parameters = [['even', 'adaptive'], [True, False], [True, False],
                  [0.0, 0.01], ['l1', 'l2']]
    list(itertools.product(*parameters))
    count = 0
    dict_list = []
    for params in itertools.product(*parameters):
      param_dict = {}
      for i, v in enumerate(params):
        param_dict[names[i]] = v
      count += 1
      dict_list.append(param_dict)
    return dict_list

  @parameterized.parameters(generate_params())
  def test_generatable_metrics(self, class_conditional, threshold, max_probs,
                               norm, binning_scheme):
    probs = np.array([[0.42610548, 0.41748077, 0.15641374],
                      [0.44766216, 0.47721294, 0.0751249],
                      [0.1862702, 0.15139402, 0.66233578],
                      [0.05753544, 0.8561222, 0.08634236],
                      [0.18697925, 0.29836466, 0.51465609]])

    labels = np.array([0, 1, 2, 1, 2])
    calibration_error = um.general_calibration_error(
        probs, labels, binning_scheme=binning_scheme, max_prob=max_probs,
        class_conditional=class_conditional, threshold=threshold, norm=norm)
    self.assertGreaterEqual(calibration_error, 0)
    self.assertLessEqual(calibration_error, 1)

if __name__ == '__main__':
  tf.enable_v2_behavior()
  tf.test.main()