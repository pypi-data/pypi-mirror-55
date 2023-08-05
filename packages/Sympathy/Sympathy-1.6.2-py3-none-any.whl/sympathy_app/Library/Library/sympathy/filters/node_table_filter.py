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
import warnings
from sympathy.api import qt2 as qt_compat
from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust
from sylib import util
from sympathy.api.exceptions import SyDataError

QtGui = qt_compat.import_module('QtGui')
QtCore = qt_compat.import_module('QtCore')
QtWidgets = qt_compat.import_module('QtWidgets')

COMMON_DOCSTRING = """
Filter the rows of Value table producing a subset as the output Filtered
table.

Filtering takes place according to a comparison relation between the
elements of two chosen columns. One of the column, Value, chosen from the
Value table that will be filtered while the other, Reference, is chosen
from the Reference table.

The comparison relation can also be defined as a lambda function in the
configuration GUI or one of the predefined relations can be used.

The predefined relations are the following:
    - In
        keeps the row from Value table if the chosen Value column is also
        present anywhere in the Reference column.

    - Not in
        keeps the row from Value table if the chosen Value column is not
        present anywhere in the Reference column.

Alternatively, a custom filter function can be defined by writing a lambda
function. The lambda function will be called once for each item in the
selected Value column with the full Reference column available under the name
`ref` (or `C0`). The lambda function should return True or False.

See https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
for a description of lambda functions. Have a look at the :ref:`Table
API<tableapi>` to see all the available methods and attributes.


.. warning::

   The labels of this node has changed. The columns Reference, Value used
   to be called C0, C1 respectively. This can be good to keep in mind if
   you are used to the old names.

"""

COLUMN_FILTERS = {
    'Match C1 in C0': 'lambda x: x in C0',
    "Don't match C1 in C0": 'lambda x: x not in C0'
}


DISPLAY = {
    'Match C1 in C0': 'In',
    "Don't match C1 in C0": 'Not in'
}


def execute_filter_query(table1, table2, parameter_root):
    c0_column_name = parameter_root['c0_column'].selected
    c1_column_name = parameter_root['c1_column'].selected

    if not (table1.is_valid() and table1.is_valid()):
        raise SyDataError('Input data is unavailable')

    if c0_column_name not in table1:
        raise SyDataError(
            f'Column: {c0_column_name} is missing in input table.')

    if c1_column_name not in table2:
        raise SyDataError(
            f'Column: {c1_column_name} is missing in input table.')

    c0_df = table1.to_dataframe()
    c1_df = table2.to_dataframe()
    # special case if incoming table has no rows

    if c0_column_name is None or c1_column_name is None:
        raise SyDataError('Selected columns are not valid.')

    c0_column = c0_df[c0_column_name]
    c1_column = c1_df[c1_column_name]
    # Expose columns as C0 and C1 when evaluating lambda function
    c0_values = c0_column.values
    c1_values = c1_column.values
    env = {
        'C0': c0_values,
        'ref': c0_values,
        'C1': c1_values,
        'val': c1_values,
    }
    use_custom_predicate = parameter_root['use_custom_predicate'].value

    if use_custom_predicate:
        predicate = util.base_eval(
            parameter_root['predicate_function'].value, env)
        selection = c1_column.apply(predicate)
    else:
        selected_filter_name = parameter_root['filter_functions'].selected
        selection = c1_column.isin(c0_column)
        if not selected_filter_name.startswith('Match'):
            selection = - selection
    return selection


def _operator_editor():
    return synode.Util.combo_editor(options=DISPLAY)


class ColumnFilterNode(synode.Node):
    __doc__ = COMMON_DOCSTRING

    name = 'Filter rows in Table'
    description = 'Filter column using Tables.'
    author = 'Alexander Busck'
    nodeid = 'org.sysess.sympathy.filters.columnfilternode'
    version = '1.1'
    icon = 'filter.svg'
    tags = Tags(Tag.DataProcessing.Select)
    related = ['org.sysess.sympathy.data.table.selecttablerows',
               'org.sysess.sympathy.data.table.selecttablerowsfromtable',
               'org.sysess.sympathy.slice.slicedatatable']

    inputs = Ports([
        Port.Table('Reference Table', name='port0'),
        Port.Table('Value Table', name='port1')])
    outputs = Ports([Port.Custom('table', 'Filtered Table', name='port0',
                                 preview=True)])

    parameters = synode.parameters()
    parameters.set_list(
        'c0_column', label='Reference',
        description=('Select the column in Reference Table, to use as '
                     'reference column in the comparison.'),
        editor=synode.Util.combo_editor(edit=True))
    parameters.set_list(
        'c1_column', label='Value',
        description=('Select the column in Value Table, to compare with '
                     'the reference column.'),
        editor=synode.Util.combo_editor(edit=True))
    parameters.set_list(
        'filter_functions', label='Operator',
        list=list(COLUMN_FILTERS.keys()),
        description='Output Value rows where',
        editor=_operator_editor())
    parameters.set_boolean(
        'use_custom_predicate', label='Use custom filter function',
        description='Use a custom filter (predicate) function to filter.')
    parameters.set_string(
        'predicate_function', label='Custom filter',
        description='The predicate function to use when filtering.',
        value='lambda val: val in ref')

    controllers = synode.controller(
        when=synode.field('use_custom_predicate', 'checked'),
        action=(synode.field('filter_functions', 'disabled'),
                synode.field('predicate_function', 'enabled')))

    def update_parameters(self, old_params):
        # Setting up editor with display.
        old_params['filter_functions'].editor = _operator_editor().value()

    def adjust_parameters(self, node_context):
        adjust(
            node_context.parameters['c0_column'], node_context.input['port0'])
        adjust(
            node_context.parameters['c1_column'], node_context.input['port1'])

    def execute(self, node_context):
        table1 = node_context.input['port0']
        table2 = node_context.input['port1']
        out_table = node_context.output['port0']
        parameters = node_context.parameters

        with warnings.catch_warnings():
            warnings.simplefilter('error', FutureWarning)

            selection = execute_filter_query(table1, table2, parameters)
            sliced_table = table2[selection]
            sliced_table.set_name(table2.get_name())
            sliced_table.set_table_attributes(table2.get_table_attributes())
            out_table.update(sliced_table)


@node_helper.list_node_decorator(['port0', 'port1'], ['port0'])
class ColumnFilterTables(ColumnFilterNode):
    name = 'Filter rows in Tables'
    nodeid = 'org.sysess.sympathy.filters.columnfiltertables'
