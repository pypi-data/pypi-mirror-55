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


class Names:
    """
    Helper class to implement names for filebase.File subclasses.
    """
    def __init__(self, kind, fields, store_created=True):
        self._store_created = store_created
        kind = kind or 'cols'

        # Compat options.
        if kind == 'calc':
            fields = 'expr'
            kind = 'cols'
        elif kind == 'col_paths':
            fields = 'path'
            kind = 'cols'

        if fields is None:
            fields = 'name'

        self._kind = kind
        self._fields = fields

        self._is_multi_fields = True
        self._fields_list = self._fields
        if self._fields is None or isinstance(self._fields, str):
            self._is_multi_fields = False
            self._fields_list = [self._fields]

        self._items = []

    def fields(self):
        return self._fields_list

    def create_item(self, item=None):
        r = dict.fromkeys(self._fields_list)
        if item:
            r.update(item)
        if self._store_created:
            self._items.append(r)
        return r

    def updated_args(self):
        """
        Used primarily to get the updated arguments after applying compat
        options.
        """
        return self._kind, self._fields

    def item_to_result(self, data):
        res = data
        if not self._is_multi_fields:
            res = data[self._fields]
        return res

    def created_items_to_result_list(self):
        data_list = self._items
        res = data_list
        if not self._is_multi_fields:
            res = []
            for row in data_list:
                res.append(row[self._fields])
        return res


def names(kind, fields, store_created=True):
    return Names(kind, fields, store_created=True)
