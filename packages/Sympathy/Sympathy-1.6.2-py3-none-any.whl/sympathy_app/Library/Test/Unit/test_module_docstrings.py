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
import ast
import os.path
import fnmatch
import unittest


def _sylib_root_path():
    """Return the path to the library's root directory."""
    sylib_root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir))
    return sylib_root_dir


def _gen_files(root):
    for curr_dir, dirs, files in os.walk(root):
        for python_file in fnmatch.filter(files, "node_*.py"):
            absolute_path = os.path.normpath(
                os.path.join(curr_dir, python_file))
            yield absolute_path


class TestNodeSource(unittest.TestCase):
    """
    Run some sanity checks on the node source code.
    """

    def test_lineendings(self):
        """Node modules should not have module level docstrings."""
        files_with_module_docstrings = []

        for f in _gen_files(_sylib_root_path()):
            try:
                mod = ast.parse(open(f).read())
                if ast.get_docstring(mod):
                    files_with_module_docstrings.append(f)
            except (IOError, OSError):
                pass

        # TODO: This limit should be lowered until it is at zero.
        if len(files_with_module_docstrings) > 62:

            assert not files_with_module_docstrings, (
                "Module docstrings in {} node modules:\n{}".format(
                    len(files_with_module_docstrings),
                    "\n".join(files_with_module_docstrings)))
