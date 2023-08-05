# Copyright (c) 2016-2017, Combine Control Systems AB
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
import json

from sympathy.api import node as synode
from sympathy.api import dtypes
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags

from sympathy.platform.editors.table_editor import TableWidget, JsonTableModel


class CreateTableConfigWidget(TableWidget):
    """
    Makes CreateTableWidget usable as a configuration gui for sympathy nodes
    hiding the parameters api from the CreateTableWidget implementation.
    """

    def __init__(self, parameters):
        self._parameters = parameters
        data = json.loads(parameters['json_table'].value)
        super().__init__(data)

    def save_parameters(self):
        data = [(name, dtypes.dtype(t).kind, rows) for name, t, rows in
                self.model().get_data()]
        self._parameters['json_table'].value = json.dumps(
            data)


class CreateTable(synode.Node):
    """
    By default the created Table will be empty so to add data to it you first
    need to create at least one column and then add at least one row.

    The name and type of a column can be changed at any time from the context
    menu of the column header.

    Cells can be masked or unmasked from the context menu of a cell or a
    selection of many cells.
    """

    name = 'Manually Create Table'
    description = 'Create a Table from scratch in a configuration Gui.'
    author = 'Magnus Sandén'
    version = '1.0'
    icon = 'create_table.svg'
    tags = Tags(Tag.Input.Generate)

    nodeid = 'org.sysess.sympathy.create.createtable'
    outputs = Ports([Port.Table('Manually created table', name='port0')])

    parameters = synode.parameters()
    parameters.set_string(
        'json_table', value='[]',
        label='GUI', description='Configuration window')

    def exec_parameter_view(self, node_context):
        return CreateTableConfigWidget(node_context.parameters)

    def execute(self, node_context):
        out_table = node_context.output['port0']
        json_data = node_context.parameters['json_table'].value
        model = JsonTableModel(json.loads(json_data))
        for name, data in model.numpy_columns():
            out_table.set_column_from_array(name, data)
