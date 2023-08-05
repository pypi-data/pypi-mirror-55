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
#     * Neither the name of Combine Control Systems AB nor the
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

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)
from sympathy.api import node
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api.exceptions import SyNodeError

import numpy as np
from scipy.spatial.distance import cdist


class DistanceMatrix(node.Node):
    """
    Computes a distance matrix between each pair of rows in two tables.

    Each row corresponds to a vector of length N where N is the number of
    columns each table. Metrics for calculation include Euclidean (default),
    City-block (aka. Manhattan) distance, and more. Hamming distance is not
    recommended for float data.
    """

    author = 'Mathias Broxvall'
    version = '0.1'
    icon = 'distance_matrix.svg'
    description = ('Computes a distance matrix between each pair of rows\n'
                   'in two tables. Each row corresponds to a vector of\n'
                   'length N where N is the number of columns each table.')
    name = 'Distance Matrix'
    tags = Tags(Tag.Analysis.Features)
    future_nodeid = 'se.combine.sympathy.dataanalysis.distance_matrix'

    parameters = node.parameters()
    parameters.set_string(
        'metric', value='euclidean', label='Metric',
        description=(
            'Metric used for comparing keypoints. '
            'See http://scipy.spatial.distance.cdist for details.'),
        editor=node.Util.combo_editor(
            options=['euclidean', 'cityblock', 'correlation', 'minkowski',
                     'hamming', 'braycurtis', 'canberra',
                     'chebyshev', 'cosine', 'dice', 'hamming', 'jaccard',
                     'kulsinski', 'mahalanobis', 'matching', 'rogerstanimoto',
                     'russellrao', 'seuclidean', 'sokalmichener',
                     'sokalsneath', 'sqeuclidean', 'wminkowski', 'yule'])
    )
    parameters.set_integer(
        'p', value=2, label='P',
        description='P norm to apply for minkowski metrics')

    inputs = Ports([
        Port.Table('Input 1', name='input 1'),
        Port.Table('Input 2', name='input 2'),
    ])
    outputs = Ports([
        Port.Table('Table with results', name='result'),
    ])

    def execute(self, node_context):
        input1      = node_context.input['input 1']
        input2      = node_context.input['input 2']
        output      = node_context.output['result']
        pnorm       = node_context.parameters['p'].value
        metric      = node_context.parameters['metric'].value

        desc1 = np.column_stack([col.data for col in input1.cols()])
        desc2 = np.column_stack([col.data for col in input2.cols()])

        if desc1.shape[1] != desc2.shape[1]:
            raise SyNodeError(
                "Number of columns does not match in the two tables")

        distances = cdist(desc1, desc2, metric=metric, p=pnorm)
        for i in range(desc2.shape[0]):
            output.set_column_from_array('{}'.format(i+1), distances[:, i])
