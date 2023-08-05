# Copyright (c) 2016, Combine Control Systems AB
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
This module contains classes that wrap tables or lists of tables for use in
various function selector, F(x), nodes in Sympathy for Data.
"""
from sympathy.platform import exceptions as syexceptions
from sympathy.utils.context import deprecated_warn


class Fx(object):
    """
    Fx should be used as the parent class for classes to be used
    in the generic F(x) nodes.

    execute is the method with will be called and it can be regarded as the
    function wrapped.
    arg_types is a list with string types as shown in port tooltips
    and it determines the types of data that the function is compatible with.

    When subclassing and creating your own function make sure to override both
    arg_types and execute.
    """
    arg_types = ['<a>']
    list_wrapper = False

    def __init__(self, arg, res, extra_arg=None):
        self.res = res
        self.arg = arg
        # Extra arg is never used.
        self.extra_arg = None
        if self.list_wrapper:
            deprecated_warn('Using list_wrapper = True '
                            'is no longer supported and has no useful effect')

    def execute(self):
        """
        Execute is called from F(x) or F(x) List nodes.

        Access input and output data using self.res and self.arg respectively.
        Override this function to provide a useful behavior.
        """
        raise syexceptions.SyConfigurationError(
            "This f(x) script doesn't implement an execute method.")


class FxWrapper(Fx):
    pass


class FxArg(Fx):

    def __init__(self, arg, res, extra_arg=None):
        super().__init__(arg, res, extra_arg=extra_arg)

    def execute(self):
        self.function(self.arg, self.res)


def decorator(arg_types):
    def inner(func):
        return type(f'Fx_{func.__name__}_cls', (FxArg,), {
            'arg_types': arg_types,
            'list_wrapper': False,
            'function': lambda self, arg, res: func(arg, res)})
    return inner
