# Copyright (c) 2017 Combine Control Systems AB
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
from __future__ import (print_function, division, unicode_literals,
                        absolute_import)
import os

from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api.exceptions import SyDataError, sywarn

from sympathy.utils import filebase
import sympathy


def filename_str(filename_syd):
    res = filename_syd.decode_path()

    if not res:
        raise SyDataError(
            'FILE datasource must be used to select file.')
    return res


def check_type(const, data):
    dtype = data.container_type
    ctype = const.container_type

    if dtype != ctype:
        raise SyDataError(
            'Type of select file: {} does not match type constraint: {}.'
            .format(dtype, ctype))


scheme = 'hdf5'


class DebugExport(synode.Node):
    """
    This is not a regular export node. The exported file will not be readable
    in any other Sympathy version than the one in which they were exported. If
    you want to export data to sydata files and be able to use the files
    between Sympathy versions you should use :ref:`Export Tables`, :ref:`Export
    ADAFs` etc.

    On the other hand this node is able to export any data type into a sydata
    file, which can be useful for debugging purposes.
    """

    name = 'Debug Export'
    description = (
        'Export internal data structure. '
        'It will only be readable in this Sympathy version.')
    icon = 'debug_export.svg'
    nodeid = 'org.sysess.sympathy.debug.export'
    author = 'Erik der Hagopian'
    version = '1.0'
    tags = Tags(Tag.Development.Debug)
    related = ['org.sysess.sympathy.debug.import']

    inputs = Ports([
        Port.Custom('<a>', 'Data', name='data'),
        Port.Datasource('Filename', name='filename')])

    outputs = Ports([
        Port.Datasource('Filename', name='filename', n=(0, 1, 0))])

    def execute(self, node_context):
        sywarn(self.description)
        data = node_context.input['data']
        fn = filename_str(node_context.input['filename'])

        with filebase.to_file(
                fn, scheme, data.container_type, external=True) as f:
            f.source(data)

        fns = node_context.output.group('filename')
        if fns:
            fns[0].encode_path(fn)


class DebugImport(synode.Node):
    """
    This is not a regular import node. The files to be imported must be created
    by :ref:`org.sysess.sympathy.debug.export` on the same Sympathy version. If
    you just want to read normal exported sydata files you should use
    :ref:`Table`, :ref:`ADAF` etc.

    On the other hand this node is able to import any data type from a sydata
    file, which can be useful for debugging purposes.
    """

    name = 'Debug Import'
    description = (
        'Import internal data structure created by Debug Export. '
        'Can only read files exported in this Sympathy version.')
    icon = 'debug_import.svg'
    nodeid = 'org.sysess.sympathy.debug.import'
    author = 'Erik der Hagopian'
    version = '1.0'
    tags = Tags(Tag.Development.Debug)
    related = ['org.sysess.sympathy.debug.export']

    inputs = Ports([
        Port.Datasource('Filename', name='filename'),
        Port.Custom('<a>', 'Type constraint', name='type', n=(1, 1, 1))])

    outputs = Ports([
        Port.Custom('<a>', 'Data', name='data')])

    def execute(self, node_context):
        sywarn(self.description)
        data = node_context.output['data']
        const = node_context.input['type']
        fn = filename_str(node_context.input['filename'])

        if not os.path.isfile(fn):
            raise SyDataError('File: {} does not exist.'.format(fn))

        fileinfo = filebase.fileinfo(fn, scheme)

        if not fileinfo.platform_version() == sympathy.__version__:
            raise SyDataError(
                'File: {} was not created with the current Sympathy'
                ' version.'.format(fn))

        with filebase.from_file(fn, scheme=scheme, external=False) as f:
            check_type(f, const)

        with filebase.from_file(
                fn, scheme, data.container_type,
                external=False) as f:
            if f.container_type != const.container_type:
                check_type(const)
            data.source(f)
