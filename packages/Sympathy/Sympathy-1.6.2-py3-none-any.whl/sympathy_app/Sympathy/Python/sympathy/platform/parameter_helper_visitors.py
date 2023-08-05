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
from sympathy.utils.context import trim_doc
from sympathy.utils.context import indent_doc


class IParameterVisitor(object):
    def visit_root(self, root):
        pass

    def visit_group(self, group):
        pass

    def visit_page(self, page):
        pass

    def visit_integer(self, value):
        pass

    def visit_float(self, value):
        pass

    def visit_string(self, value):
        pass

    def visit_boolean(self, value):
        pass

    def visit_datetime(self, value):
        pass

    def visit_list(self, plist):
        pass

    def visit_json(self, value):
        pass

    def visit_custom(self, custom):
        pass


class ShowParameterVisitor(object):
    """
    Builds a string of all visited parameter leaf entities, the string result
    is available in instance.result. The format of the string compatible with
    the documentation format used, and is valid Restructured Text.

    This useful for generating the documentation for the configuration options.
    """
    def __init__(self):
        self.result = None

    def visit_root(self, root):
        self.visit_group(root)

    def visit_group(self, group):
        results = []
        for item in group.children():
            visitor = ShowParameterVisitor()
            item.accept(visitor)
            results.append(visitor.result)
        self.result = u'\n'.join(results)

    def visit_page(self, page):
        self.visit_group(page)

    def visit_integer(self, value):
        self.visit_value(value)

    def visit_float(self, value):
        self.visit_value(value)

    def visit_string(self, value):
        self.visit_value(value)

    def visit_boolean(self, value):
        self.visit_value(value)

    def visit_datetime(self, value):
        self.visit_value(value)

    def visit_json(self, value):
        self.visit_value(value)

    def visit_list(self, plist):
        self.visit_value(plist)

    def visit_value(self, value):
        self.result = u'**{}** ({})\n{}'.format(
            value.label or '(no label)',
            value.name,
            indent_doc(
                trim_doc(value.description or '(no description)'), 4))


class ReorderVisitor(IParameterVisitor):
    """Order elements."""
    def visit_root(self, root):
        self.visit_group(root)

    def visit_group(self, group):
        group.reorder()
        for item in group.children():
            item.accept(self)

    def visit_page(self, page):
        self.visit_group(page)
