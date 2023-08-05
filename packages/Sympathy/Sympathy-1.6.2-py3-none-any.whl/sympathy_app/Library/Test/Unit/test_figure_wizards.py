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
import copy
import unittest

from sylib.figure import gui, models
from sympathy.api import table


class TestWizards(unittest.TestCase):
    def test_wizard_models(self):
        self.maxDiff = None
        empty_model = models.Root({})
        data_table = table.File()
        empty_model.set_data_table(data_table)

        wizard_configs = {
            gui.ScatterWizard: [
                {
                    'x_signal': 'a',
                    'y_signal': 'b',
                }, {
                    'x_signal': 'a',
                    'y_signal': 'b',
                    'colors': 'c',
                    'sizes': 'd',
                }],
            gui.LineWizard: [
                {
                    'x_signal': 'a',
                    'y_signals': ['b'],
                }, {
                    'x_signal': 'a',
                    'y_signals': ['b', 'c'],
                }],
            gui.BarWizard: [
                {
                    'bin_labels': 'a',
                    'y_signals': ['b'],
                }, {
                    'bin_labels': 'a',
                    'y_signals': ['b', 'c'],
                }],
            gui.PieWizard: [
                {
                    'labels': 'a',
                    'values': 'b',
                }],
            gui.BoxWizard: [
                {
                    'signals': ['a'],
                }, {
                    'signals': ['a', 'b'],
                }],
        }

        for wizard_cls, configs in wizard_configs.items():
            for config in configs:
                wizard = wizard_cls(empty_model)
                for param, value, in config.items():
                    if wizard._parameters[param].type == 'list':
                        wizard._parameters[param].value_names = value
                    else:
                        wizard._parameters[param].value = value
                wiz_model = wizard.get_model()
                model_root = models.Root(copy.deepcopy(wiz_model))
                model_root.set_data_table(data_table)
                new_model = model_root.export_config()
                self.assertEqual(wiz_model, new_model)

#     def test_parse_configuration(self):
#         self.maxDiff = None
#         parsed_config = parse_configuration(copy.deepcopy(self.stored_config))
#         self.assertDictEqual(self.parsed_config, parsed_config)

#     def test_export_config(self):
#         model = gui.DataModel(copy.deepcopy(self.parsed_config))
#         font_nodes = model.root.find_all_nodes_with_class(models.BarLabelsFont)
#         self.assertEqual(len(font_nodes), 2)
#         exported_config = sorted(export_config(model))
#         stored_config = sorted(self.stored_config)
#         self.maxDiff = None
#         self.assertEqual(exported_config, stored_config)
#         self.assertEqual(len(exported_config), len(stored_config))


# def runModelTest():  # noqa
#     test_loader = unittest.TestLoader()
#     test_loader.loadTestsFromTestCase(ParseStringToMPLColorTestCase)
#     test_loader.loadTestsFromTestCase(ParseConfigurationTestCase)
#     unittest.TextTestRunner(verbosity=2)
