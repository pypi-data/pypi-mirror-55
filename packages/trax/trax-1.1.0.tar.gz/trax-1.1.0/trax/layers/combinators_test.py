# coding=utf-8
# Copyright 2019 The Trax Authors.
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

"""Tests for combinator layers."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from trax import backend
from trax.layers import base
from trax.layers import combinators as cb
from trax.layers import core
from trax.shapes import ShapeDtype


class CombinatorLayerTest(absltest.TestCase):

  def test_drop(self):
    layer = cb.Drop()
    input_signature = ShapeDtype((3, 2))
    expected_shape = ()
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_dup(self):
    layer = cb.Dup()
    input_signature = ShapeDtype((3, 2))
    expected_shape = ((3, 2), (3, 2))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_swap(self):
    layer = cb.Swap()
    input_signature = (ShapeDtype((3, 2)), ShapeDtype((4, 7)))
    expected_shape = ((4, 7), (3, 2))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_serial_no_op(self):
    layer = cb.Serial(None)
    input_signature = (ShapeDtype((3, 2)), ShapeDtype((4, 7)))
    expected_shape = ((3, 2), (4, 7))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_serial_no_op_list(self):
    layer = cb.Serial([])
    input_signature = (ShapeDtype((3, 2)), ShapeDtype((4, 7)))
    expected_shape = ((3, 2), (4, 7))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_serial_one_in_one_out(self):
    layer = cb.Serial(core.Div(divisor=2.0))
    input_signature = ShapeDtype((3, 2))
    expected_shape = (3, 2)
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_serial_div_div(self):
    layer = cb.Serial(core.Div(divisor=2.0), core.Div(divisor=5.0))
    input_signature = ShapeDtype((3, 2))
    expected_shape = (3, 2)
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_serial_dup_dup(self):
    layer = cb.Serial(cb.Dup(), cb.Dup())
    input_signature = ShapeDtype((3, 2))
    expected_shape = ((3, 2), (3, 2), (3, 2))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_parallel_dup_dup(self):
    layer = cb.Parallel(cb.Dup(), cb.Dup())
    input_signature = (ShapeDtype((3, 2)), ShapeDtype((4, 7)))
    expected_shape = ((3, 2), (3, 2), (4, 7), (4, 7))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_parallel_div_div(self):
    layer = cb.Parallel(core.Div(divisor=0.5), core.Div(divisor=3.0))
    input_signature = (ShapeDtype((3, 2)), ShapeDtype((4, 7)))
    expected_shape = ((3, 2), (4, 7))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_parallel_no_ops(self):
    layer = cb.Parallel([], None)
    input_signature = (ShapeDtype((3, 2)), ShapeDtype((4, 7)))
    expected_shape = ((3, 2), (4, 7))
    output_shape = base.check_shape_agreement(layer, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_branch_op_not_defined(self):
    with self.assertRaises(AttributeError):
      cb.Branch([], [])

  def test_scan_basic(self):
    @base.layer(n_in=2, n_out=2)
    def add(x, **unused_kwargs):
      res = x[0] + x[1]
      return res, res
    scan_layer = cb.Scan(add())  # pylint: disable=no-value-for-parameter
    input_signature = (ShapeDtype((3, 2, 7)), ShapeDtype((2, 7)))
    expected_shape = ((3, 2, 7), (2, 7))
    output_shape = base.check_shape_agreement(scan_layer, input_signature)
    self.assertEqual(output_shape, expected_shape)
    inp = (backend.numpy.array([1, 2, 3]), backend.numpy.array(0))
    o, v = scan_layer(inp)
    self.assertEqual(int(v), 6)
    self.assertEqual([int(x) for x in o], [1, 3, 6])

  def test_scan_axis1(self):
    @base.layer(n_in=2, n_out=2)
    def add(x, **unused_kwargs):
      res = x[0] + x[1]
      return res, res
    scan = cb.Scan(add(), axis=1)  # pylint: disable=no-value-for-parameter
    input_signature = (ShapeDtype((3, 2, 7)), ShapeDtype((3, 7)))
    expected_shape = ((3, 2, 7), (3, 7))
    output_shape = base.check_shape_agreement(scan, input_signature)
    self.assertEqual(output_shape, expected_shape)

  def test_scan_multiinput(self):
    @base.layer(n_in=3, n_out=2)
    def foo(x, **unused_kwargs):
      a, b, carry = x
      return a + b, b, carry + 1
    scan = cb.Scan(foo(), axis=1)  # pylint: disable=no-value-for-parameter
    input_signature = (ShapeDtype((3, 2, 7)), ShapeDtype((3, 2, 7)),
                       ShapeDtype((3, 7)))
    expected_shape = ((3, 2, 7), (3, 2, 7), (3, 7))
    output_shape = base.check_shape_agreement(scan, input_signature)
    self.assertEqual(output_shape, expected_shape)


if __name__ == '__main__':
  absltest.main()
