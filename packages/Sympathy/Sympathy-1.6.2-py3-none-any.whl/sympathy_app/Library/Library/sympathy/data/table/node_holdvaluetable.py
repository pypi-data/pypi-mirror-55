# -*- coding:utf-8 -*-
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
import numpy as np
from sympathy.api import node
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust


def hold_column(array):
    missing = []
    if array.dtype.kind == 'f':
        missing = np.where(np.isnan(array))[0]
    elif array.dtype.kind in ['m', 'M']:
        missing = np.where(np.isnat(array))[0]

    mask = None

    if isinstance(array, np.ma.core.MaskedArray):
        for i in np.where(~array.mask)[0]:
            if i > 0:
                mask = np.zeros(len(array), dtype=bool)
                mask[:i] = True
            break

        idx = set()
        maskidx = np.flatnonzero(array.mask)

        idx.update(maskidx)
        idx.update(missing)
        missing = sorted(set(idx))

    it = iter(missing)

    try:
        i = next(it)
    except StopIteration:
        return array

    # Local copy for in-place edit.
    array = np.array(array)

    if i != 0:
        array[i] = array[i - 1]

    for i in it:
        array[i] = array[i - 1]

    if mask is not None:
        return np.ma.MaskedArray(array, mask)

    return array


def hold_table(in_table, out_table, hold_cnames):
    for cname in in_table.column_names():
        if cname in hold_cnames:
            out_table.set_column_from_array(
                cname, hold_column(in_table.get_column_to_array(cname)))
            out_table.set_column_attributes(
                cname, in_table.get_column_attributes(cname))
        else:
            out_table.update_column(cname, in_table)

    out_table.set_table_attributes(in_table.get_table_attributes())
    out_table.name = in_table.name


class HoldValueTable(node.Node):
    """
    Replace occurences of nan in cells by the last non-nan value from the same
    column.
    """
    author = 'Erik der Hagopian'
    version = '1.0'
    icon = 'drop_nan.svg'
    tags = Tags(Tag.DataProcessing.TransformData)
    description = (
        'Replace occurences of nan in cells by the last non-nan value from '
        'the same column.')
    related = ['org.sysess.sympathy.data.table.holdvaluetables',
               'org.sysess.sympathy.data.table.dropnantable']

    name = 'Hold value Table'
    nodeid = 'org.sysess.sympathy.data.table.holdvaluetable'

    inputs = Ports([
        Port.Table('Input Table')])
    outputs = Ports([
        Port.Table('Output Table with NaN replaced')])

    parameters = node.parameters()
    parameters.set_list(
        'columns', label='Select columns', description='Select columns.',
        value=[], editor=node.Editors.multilist_editor(edit=True))
    parameters['columns']._passthrough = True

    def adjust_parameters(self, ctx):
        adjust(ctx.parameters['columns'], ctx.input[0])

    def execute(self, ctx):
        in_table = ctx.input[0]
        out_table = ctx.output[0]
        cols = ctx.parameters['columns'].selected_names(
            in_table.column_names())
        hold_table(in_table, out_table, cols)


@node_helper.list_node_decorator([0], [0])
class HoldValueTables(HoldValueTable):
    name = 'Hold value Tables'
    nodeid = 'org.sysess.sympathy.data.table.holdvaluetables'
