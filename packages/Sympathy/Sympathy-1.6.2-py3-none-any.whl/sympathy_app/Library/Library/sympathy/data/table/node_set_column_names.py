# Copyright (c) 2019 Combine Control Systems AB
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

from sympathy.api import node
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust
from sympathy.api.exceptions import SyDataError
from sympathy.api import node_helper


class SetColumnNamesInTableWithTable(node.Node):
    """
    Set column names in data table to new names from chosen column in the name
    table.

    Since the new names are assigned based on indices, the number of rows in
    the name column must match the number of columns in the data table.


    Example
    ^^^^^^^

    Input data:

    +---+---+---+
    | A | B | C |
    +===+===+===+
    | 0 | 1 | 2 |
    +---+---+---+


    Input names:

    +-------+
    | Names |
    +=======+
    |   X   |
    +-------+
    |   Y   |
    +-------+
    |   Z   |
    +-------+


    Output data:

    +---+---+---+
    | X | Y | Z |
    +===+===+===+
    | 0 | 1 | 2 |
    +---+---+---+

    """

    name = 'Set column names in Table with Table'
    description = 'Set column names from separate table column.'
    nodeid = 'org.sysess.sympathy.setcolumnnamesintablewithtable'
    author = 'Erik der Hagopian'
    icon = 'rename_columns.svg'
    version = '1.0'
    tags = Tags(Tag.DataProcessing.TransformStructure)

    related = ['org.sysess.sympathy.data.table.renametablecolumnstable']

    parameters = node.parameters()
    parameters.set_string(
        'name', label='New names',
        description='Column with new names',
        editor=node.editors.combo_editor())

    inputs = Ports([
        Port.Table('Data', name='data'),
        Port.Table('Name', name='name')])
    outputs = Ports([
        Port.Table('Data', name='data')])

    def adjust_parameters(self, ctx):
        adjust(ctx.parameters['name'], ctx.input['name'])

    def execute(self, ctx):
        in_data_table = ctx.input['data']
        in_name_table = ctx.input['name']
        out_data_table = ctx.output['data']

        key = ctx.parameters['name'].value

        if not key:
            raise SyDataError('Please select names column.')
        elif key not in in_name_table:
            raise SyDataError('Selected name column does not exist.')

        if in_data_table.number_of_columns() != in_name_table.number_of_rows():
            raise SyDataError(
                "Number of name rows must be the same as the number of data "
                "columns.")

        name_col = in_name_table[key]

        if len(set(name_col)) != len(name_col):
            raise SyDataError('All new names must be unique.')

        out_data_table.name = in_data_table.name
        out_data_table.name = in_data_table.name
        out_data_table.set_table_attributes(
            in_data_table.get_table_attributes())

        for new_name, old_name in zip(name_col, in_data_table.column_names()):
            out_data_table.update_column(new_name, in_data_table, old_name)


@node_helper.list_node_decorator(['data'], ['data'])
class SetColumnNamesInTablesWithTable(SetColumnNamesInTableWithTable):
    name = 'Set column names in Tables with Table'
    description = 'Set column names from separate table column.'
    nodeid = 'org.sysess.sympathy.setcolumnnamesintableswithtable'
