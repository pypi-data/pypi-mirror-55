# -*- coding:utf-8 -*-
# Copyright (c) 2017, Combine Control Systems AB
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
from sympathy.api import fx_wrapper, fx


class GenericPrintCalculation(fx_wrapper.FxWrapper):
    arg_types = ['<a>']

    def execute(self):
        # See the Table API description in the Help (under Data type
        # APIs) for more information on how to write functions.
        print('Forwarding arg: {}'.format(type(self.arg).__name__))
        self.res.source(self.arg)


class SingleSpamCalculation(fx.Fx):
    arg_types = ['table']

    def execute(self):
        # See the ADAF API description in the Help (under Data type
        # APIs) for more information on how to write functions.

        spam = self.arg['spam']

        # My super advanced calculation that totally couldn't be
        # done in the :ref:`Calculator` node:
        more_spam = spam + 1
        self.res['more spam'] = more_spam
        print('more spam')


@fx.decorator(['table'])
def single_spam_function(arg, res):
    spam = arg['spam']

    # My super advanced calculation that totally couldn't be
    # done in the :ref:`Calculator Lists` node:
    more_spam = spam + 1

    res['more spam'] = more_spam
    print('more spam')
