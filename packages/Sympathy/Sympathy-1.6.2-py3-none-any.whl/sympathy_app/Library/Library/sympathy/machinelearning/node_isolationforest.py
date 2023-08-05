# Copyright (c) 2017, Combine Control Systems AB
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Combine Control Systems AB nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL COMBINE CONTROL SYSTEMS AB BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Some of the docstrings for this module have been automatically
extracted from the `scikit-learn <http://scikit-learn.org/>`_ library
and are covered by their respective licenses.
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)
import warnings

import sklearn
# Ignore a warning from numpy>=1.15.2 when importing sklearn.ensemble
# See issue #2768 for details.
with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
    import sklearn.ensemble

from sympathy.api import node
from sympathy.api.nodeconfig import Ports, Tag, Tags

from sylib.machinelearning.model import ModelPort
from sylib.machinelearning.abstract_nodes import SyML_abstract
from sylib.machinelearning.decisiontrees import IsolationForestDescriptor

from sylib.machinelearning.descriptors import BoolType
from sylib.machinelearning.descriptors import FloatType
from sylib.machinelearning.descriptors import IntType
from sylib.machinelearning.descriptors import NoneType
from sylib.machinelearning.descriptors import StringSelectionType
from sylib.machinelearning.descriptors import UnionType


class IsolationForest(SyML_abstract, node.Node):
    name = 'Isolation Forest'
    author = 'Mathias Broxvall'
    version = '0.1'
    icon = 'isolation_forest.svg'
    description = (
        'Predicts outliers based on minimum path length of random trees with '
        'single nodes in the leafs.')
    nodeid = 'org.sysess.sympathy.machinelearning.isolation_forest'
    tags = Tags(Tag.MachineLearning.Unsupervised)

    descriptor = IsolationForestDescriptor()
    descriptor.name = name
    descriptor.set_info([
        {'name': 'n_estimators',
         'type': IntType(min_value=0, default=100)},
        {'name': 'max_samples',
         'type': UnionType([
             IntType(),
             FloatType(),
             StringSelectionType(['auto'])],
                           default='auto'),
         'desc': (
             'The number of samples to draw from X to train each base '
             'estimator  expressed as number of samples (int), or a '
             'fraction of all samples (float). If "auto" then a maximum of '
             '256 samples will be used (less when fewer input samples given)'
         )},
        {'name': 'contamination',
         'type': FloatType(min_value=0, max_value=0.5, default=0.1)},
        {'name': 'max_features',
         'type': UnionType([
             IntType(min_value=1),
             FloatType(min_value=0.0, max_value=1.0)],
            default=1.0)},
        {'name': 'bootstrap',
         'type': BoolType(default=False)},
        {'name': 'n_jobs',
         'type': IntType(min_value=-1, default=1)},
        {'name': 'random_state',
         'type': UnionType([
             IntType(), NoneType()], default=None)},
    ], doc_class=sklearn.ensemble.IsolationForest)

    descriptor.set_attributes([
        {'name': 'estimators_samples_', },
        {'name': 'max_samples_'},
    ], doc_class=sklearn.ensemble.IsolationForest)

    parameters = node.parameters()
    SyML_abstract.generate_parameters(parameters, descriptor)

    inputs = Ports([])
    outputs = Ports([ModelPort('Model', 'model')])
    __doc__ = SyML_abstract.generate_docstring(
        description, descriptor.info, descriptor.attributes, inputs, outputs)

    def execute(self, node_context):
        model = node_context.output['model']
        desc = self.__class__.descriptor
        model.set_desc(desc)

        kwargs = self.__class__.descriptor.get_parameters(
            node_context.parameters)
        try:
            # Force new behavior and suppress transitional warning.
            # This option will be removed in 0.24.
            # Exact result will depend on version used.
            skl = sklearn.ensemble.IsolationForest(behaviour='new', **kwargs)
        except TypeError:
            skl = sklearn.ensemble.IsolationForest(**kwargs)

        model.set_skl(skl)
        model.save()
