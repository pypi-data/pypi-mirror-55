# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2017 Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import os
import io
import unittest
from lxml import etree

from Gui.flowview import port_icon
from Gui.datatypes import DataType

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def elements_equal(e1, e2):
    # https://stackoverflow.com/questions/7905380/testing-equivalence-of-xml-etree-elementtree
    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))


class TestPortIcons(unittest.TestCase):

    # TODO(erik): this test expects checks against hard-coded output
    # from svgutils 0.2 and svgutils 0.3; it may fail with other versions of
    # svgutils.

    def test_porticons(self):
        expected_results = {}
        svgutils_versions = ['0.2', '0.3']

        for svgutils_version in svgutils_versions:
            path = os.path.join(
                TEST_DIR, 'expected_porticon_svgutils_{}.svg'.format(
                    svgutils_version))
            with open(path) as f:
                expected_results[svgutils_version] = f.read().encode('ascii')

        type_ = (                                                       # noqa
            '('                                                         # noqa
                'datasource,'                                           # noqa
                '['                                                     # noqa
                    '('                                                 # noqa
                        '['                                             # noqa
                            '(datasource, figure)], '                   # noqa
                            '('                                         # noqa
                                '(table, adaf -> text), '               # noqa
                                '('                                     # noqa
                                    '(table, adaf -> text), '           # noqa
                                    '('                                 # noqa
                                        '(report, unknown), '           # noqa
                                        '('                             # noqa
                                            '(report, unknown), '       # noqa
                                            '('                         # noqa
                                                '(), '                  # noqa
                                                'lambda'                # noqa
                                            ')'                         # noqa
                                        ')'                             # noqa
                                    ')'                                 # noqa
                                ')'                                     # noqa
                            ')'                                         # noqa
                        ')'                                             # noqa
                    ']'                                                 # noqa
            ')')                                                        # noqa
        icons = {
            'figure': 'ports/figure.svg',
            'text': 'ports/text.svg',
            'table': 'ports/table.svg',
            'datasource': 'ports/datasource.svg',
            'adaf': 'ports/adaf.svg',
            'report': 'ports/report.svg',
            'unknown': 'ports/unknown.svg',
            'lambda': 'ports/lambda.svg'}
        datatype = DataType.from_str(type_)
        svg = port_icon.icon(datatype._datatype, icons)

        if svg not in list(expected_results.values()):
            equal = None
            for svgutils_version in svgutils_versions:
                ref = expected_results[svgutils_version]
                ref_xml = etree.parse(io.BytesIO(ref))
                svg_xml = etree.parse(io.BytesIO(svg))
                if elements_equal(svg_xml.getroot(), ref_xml.getroot()):
                    equal = svgutils_version
                    break
            assert equal


if __name__ == '__main__':
    unittest.main()
