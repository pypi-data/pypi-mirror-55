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

"""Trax top level import."""

from trax import backend
from trax import inputs
from trax import layers as tl
from trax import learning_rate as lr
from trax import shapes
from trax import trainer_lib
from trax.backend import eval_on_shapes
from trax.backend import grad
from trax.backend import logsumexp
from trax.backend import numpy as np
from trax.backend import random
