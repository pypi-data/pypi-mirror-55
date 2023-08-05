# This file is part of Sympathy for Data.
# Copyright (c) 2013 Combine Control Systems AB
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
import sys
import io
import os
import jinja2
import six
import platform
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui
import Qt.QtWidgets as QtWidgets

from sympathy.utils import pip_util
from .. import version
from .. import settings


class LicenseThread(QtCore.QThread):
    license_text = QtCore.Signal(six.text_type)

    def run(self):
        with io.open(os.path.join(
                settings.instance()['resource_folder'],
                'third_party.html')) as f:
            licenses_template = f.read()

        license_text = jinja2.Template(licenses_template).render(
            pkgs=[],
            status='Generating package information, please wait.')

        self.license_text.emit(license_text)

        reqs = os.path.join(settings.instance()['install_folder'], 'Package',
                            'requires.txt')
        req_names = list(pip_util.requirements(reqs).keys())

        with io.open(os.path.join(
                settings.instance()['resource_folder'],
                'third_party.html')) as f:
            licenses_template = f.read()

        license_text = jinja2.Template(licenses_template).render(
            pkgs=pip_util.showall(req_names, ignore_missing=True),
            status='Generated package information:')
        self.license_text.emit(license_text)


class AboutWindow(QtWidgets.QDialog):
    """Docstring for AboutWindow"""

    def __init__(self, parent=None, flags=QtCore.Qt.Widget):
        super(AboutWindow, self).__init__(parent, flags)
        self._license_thread = LicenseThread()
        self._init()

    def _init(self):
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Sympathy for Data')
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(800, 600)
        about = '''
            <br/>
            &copy; 2011-2019 <a href={appurl}>{appcopy}</a>
            All Rights Reserved.
            This software is licensed under the
            <a href=http://www.gnu.org/copyleft/gpl.html>GPL license</a>.
            <br/><br/>
            Design and programming by:
            Stefan Larsson, Alexander Busck,
            Krister Johansson, Erik der Hagopian,
            Greger Cronquist, Magnus Sand&eacute;n,
            Daniel Hedendahl, Lia Silva-Lopez,
            Andreas T&aring;gerud, Sara Gustafzelius,
            Samuel Genheden,
            Benedikt Ziegler, and Mathias Broxvall
            <br/><br/>
            Please report bugs to:
            <a href=mailto:{mailsupport}>{mailsupport}</a>,
            contributions can be sent to:
            <a href=mailto:{mailcontrib}>{mailcontrib}</a>'''.format(
                appurl=version.application_url(),
                appcopy=version.application_copyright(),
                mailsupport=version.email_bugs(),
                mailcontrib=version.email_contribution())

        version_info = '''
            <br/><br/>
            Sympathy version: {version} ({arch} bit)<br/>
            <br/>
            Python version: {python_version}<br/>
        '''.format(
            version=version.version,
            arch=(64 if sys.maxsize > 2 ** 32 else 32),
            python_version=platform.python_version())

        self._label = QtWidgets.QLabel(about + version_info)
        self._label.setWordWrap(True)
        self._label.setOpenExternalLinks(True)

        self._license_view = QtWidgets.QTextBrowser()
        self._license_view.setOpenExternalLinks(True)
        self._license_view.setOpenLinks(True)
        self._license_view.setMinimumHeight(200)
        self._license_view.setReadOnly(True)

        self._button_box = QtWidgets.QDialogButtonBox()
        ok_button = self._button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        ok_button.clicked.connect(self.accept)

        self._logo = QtWidgets.QLabel('Sympathy for Data')
        self._label_font = QtWidgets.QApplication.font()
        self._label.setFont(self._label_font)
        self._label_font.setPointSize(36)
        self._logo.setFont(self._label_font)
        layout.addWidget(self._logo)
        layout.addWidget(self._label)
        layout.addWidget(self._license_view)
        layout.addWidget(self._button_box)

        self._license_thread.license_text.connect(self._set_license_html)
        self._license_thread.finished.connect(self._wait_license)
        self._license_thread.start()

    def _set_license_html(self, html):
        vscrollbar = self._license_view.verticalScrollBar()
        vscroll = vscrollbar.value()
        textcursor = self._license_view.textCursor()
        cursor_start = textcursor.selectionStart()
        cursor_end = textcursor.selectionEnd()
        self._license_view.setHtml(html)
        textcursor = self._license_view.textCursor()
        textcursor.setPosition(cursor_start)
        textcursor.setPosition(cursor_end, QtGui.QTextCursor.KeepAnchor)
        self._license_view.setTextCursor(textcursor)
        vscrollbar.setValue(vscroll)

    def _wait_license(self):
        self._license_thread.wait()
