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
import lxml.html

from PySide2 import QtWidgets, QtCore


def table_values_to_clipboard(values, headers=None):
    """
    Put the values into the clipboard in a format understood by many other
    applications (incl. Excel).

    values should be a list of lists of table values, where each inner list
    represents one row of values.
    """
    def escape_html(text):
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;'))

    if headers is None:
        headers = []

    if not values:
        return
    elif len(values) == 1 and len(values[0]) == 1 and not headers:
        # Only a single value was selected. Copy it without the table.
        csv = str(values[0][0])
        html = escape_html(str(values[0][0]))
    else:
        csv_lines = []
        html_lines = ['<html><body><table>']

        if headers:
            html_lines.append('<thead><tr>')
            html_lines.extend('<th>{}</th>'.format(
                escape_html(str(header))) for header in headers)
            html_lines.append('</tr></thead>')

        html_lines.append('<tbody>')
        for row_i, row in enumerate(values):
            html_row_values = []
            for col_i, value in enumerate(row):
                html_row_values.append('<td>{}</td>'.format(
                    escape_html(str(value))))

            csv_lines.append('\t'.join([str(v) for v in row]))
            html_lines.append('<tr>')
            html_lines.extend(html_row_values)
            html_lines.append('</tr>')
        html_lines.append('</tbody>')
        html_lines.append('</table></body></html>')
        csv = '\n'.join(csv_lines)
        html = '\n'.join(html_lines)

    mime_data = QtCore.QMimeData()
    mime_data.setHtml(html)
    mime_data.setText(csv)
    QtWidgets.QApplication.clipboard().setMimeData(mime_data)


def table_values_from_clipboard(return_headers=False):
    """
    Get values from the clipboard into a list of lists. Can read copied values
    from many applications, incl. Excel.

    Each inner list represents one row of values. Rows are padded if needed
    such that all rows contain the same number of values.

    If return_headers is True, a list of headers is also returned alongside the
    values.

    Note that all returned values are strings and so they might need to be
    parsed to other types.
    """
    clipboard = QtWidgets.QApplication.clipboard()
    mime_data = clipboard.mimeData()

    headers = []
    values = []
    if mime_data.hasHtml():
        html = mime_data.html()
        root = lxml.html.fromstring(html)
        table = root.find('.//table')
        if table is not None:
            # Find first tr tag with th children:
            header_line = table.find('.//tr[th]')
            if header_line is not None:
                headers = [cell.text_content().strip()
                           for cell in header_line.findall('th')]

            # Find all tr tags with td children:
            for line in table.iterfind('.//tr[td]'):
                values.append([cell.text_content().strip()
                               for cell in line.findall('td')])
        else:
            values.append([root.text_content()])
    elif mime_data.hasText():
        text = clipboard.text()
        for line in text.splitlines():
            line = line.strip()
            if line:
                values.append(line.split('\t'))

    # Pad all rows to the length of the maximum length of any row.
    if values:
        max_column_counts = max(len(row) for row in values)
        if return_headers:
            max_column_counts = max(max_column_counts, len(headers))
            headers = headers + ['']*(max_column_counts - len(headers))
        values = [row + ['']*(max_column_counts - len(row))
                  for row in values]

    if return_headers:
        return values, headers
    else:
        return values
