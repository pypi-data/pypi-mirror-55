# Copyright (c) 2013, Combine Control Systems AB
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
In various programs, like file managers or spreadsheet programs, there do
often exist a functionality, where the data is sorted according to
some specified order of a specific part of the data. This functionality
do also exist in the standard library of Sympathy for Data and is represented
by the two nodes in this category.

The rows in the Tables are sorted according to the ascending/descending order
of a specified sort column. Both the sort column and the sort order have to
be specified in configuration GUI.
"""
from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Tag, Tags, adjust, Port, Ports
import numpy as np


def _get_single_col_editor():
    return synode.Util.combo_editor('', filter=True, edit=True)


class SortRowsTable(synode.Node):
    """
    Sort table rows according to ascending/descending order of a sort
    column.
    """

    author = 'Greger Cronquist'
    version = '1.1'
    icon = 'sort_table_rows.svg'
    tags = Tags(Tag.DataProcessing.TransformStructure)

    name = 'Sort rows in Table'
    nodeid = 'org.sysess.sympathy.data.table.sorttable'

    inputs = Ports([Port.Table('Input', name='Input')])
    outputs = Ports([Port.Table('Input', name='Output')])

    editor = _get_single_col_editor()
    parameters = synode.parameters()
    parameters.set_list(
        'column', label='Sort column',
        description='Column to sort',
        editor=editor)
    parameters.set_list(
        'sort_order', label='Sort order',
        list=['Ascending', 'Descending'], value=[0],
        description='Sort order',
        editor=synode.Util.combo_editor().value())

    def update_parameters(self, old_params):
        param = 'column'
        if param in old_params:
            old_params[param].editor = _get_single_col_editor()

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['column'], node_context.input['Input'])

    def execute(self, node_context):
        in_table = node_context.input['Input']
        out_table = node_context.output['Output']
        parameters = node_context.parameters

        if in_table.is_empty():
            return

        column_name = parameters['column'].selected
        column = in_table.get_column_to_array(column_name)
        idx = np.ma.argsort(column, kind='mergesort')
        if parameters['sort_order'].selected == 'Descending':
            idx = idx[::-1]

        if isinstance(column, np.ma.MaskedArray):
            masked = np.ma.getmaskarray(column)[idx]
            if parameters['sort_order'].selected == 'Ascending':
                # Ascending: put masked values last
                idx = np.concatenate((idx[~masked], idx[masked]))
            else:
                # Descending: put masked values first
                idx = np.concatenate((idx[masked], idx[~masked]))

        for column_name in in_table.column_names():
            array = in_table.get_column_to_array(column_name)
            out_table.set_column_from_array(column_name, array[idx])

        out_table.set_attributes(in_table.get_attributes())
        out_table.set_name(in_table.get_name())


@node_helper.list_node_decorator(['Input'], ['Output'])
class SortRowsTables(SortRowsTable):
    name = 'Sort rows in Tables'
    nodeid = 'org.sysess.sympathy.data.table.sorttables'
