# -*- coding: utf-8 -*-
# Copyright (c) 2019, Combine Control Systems AB
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
from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust

import pandas as pd


class UnpivotTable(synode.Node):
    """
    Unpivot a Table.

    The inverse operation of Pivot Table. The operation transforms data from a 
    wide to a narrow format. The wide form can be considered as a matrix of 
    column values, while the narrow form is a natural encoding of a sparse 
    matrix. When the data types of value columns differ, the varying data is 
    converted to a common data type so the source data can be part of one 
    single column in the new data set.

    """

    name = 'Unpivot Table'
    nodeid = 'org.sysess.sympathy.data.table.unpivottablenode'
    author = 'Emil Staf'
    version = '0.1'
    icon = 'pivot_table.svg'
    tags = Tags(Tag.DataProcessing.TransformStructure)

    inputs = Ports([Port.Table('Input Table', name='Input')])
    outputs = Ports([Port.Table('Output Table', name='Output')])

    parameters = synode.parameters()
    parameters.set_string('index',
        label='Index column',
        value='',
        description='Column that contains a unique identifier for each row',
        editor=synode.editors.combo_editor(include_empty=True, edit=True))

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['index'],
               node_context.input['Input'])

    def execute(self, node_context):
        
        in_table = node_context.input['Input']
        if in_table.is_empty():
            return

        columns = node_context.input['Input'].column_names()

        out_table = node_context.output['Output']
        parameters = node_context.parameters
        
        df = in_table.to_dataframe()

        # order the columns to match order in in_table
        df = df[columns]
        
        # Find index column
        index_col = parameters['index'].value
        if not index_col:
            df['index'] = df.index
            index_col = 'index'

        # value_vars = df.loc[:, df.columns != index_col]
        value_vars = [c for c in columns if c != index_col]

        # Unpivot happens here
        df_out = pd.melt(df, id_vars=[index_col], value_vars=value_vars)

        # rename to match Pivot Table
        df_out = df_out.rename(columns={'variable': 'Column names'})

        # Create new table from DataFrame
        out_table_df = out_table.__class__.from_dataframe(df_out)

        # Write to output table
        out_table.source(out_table_df)

        # set table name using in table
        out_table.set_name(in_table.get_name())


@node_helper.list_node_decorator(['Input'], ['Output'])
class UnpivotTables(UnpivotTable):
    name = 'Unpivot Tables'
    nodeid = 'org.sysess.sympathy.data.table.unpivottablesnode'
