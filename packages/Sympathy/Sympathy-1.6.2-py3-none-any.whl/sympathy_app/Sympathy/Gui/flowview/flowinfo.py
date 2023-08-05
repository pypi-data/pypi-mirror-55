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
import json
import cgi
import re
import os.path

import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets

from sympathy.utils import uuid_generator
from sympathy.utils import prim
from sympathy.platform.widget_library import (PathListWidget, PathLineEdit,
                                              StackedTextViews)
from sympathy.platform import widget_library as sywidgets
from sympathy.utils import library_info

from .types import get_label
from .. import util
from .. import settings
from Gui import user_commands
from Gui.windows import preferences
import Gui.library


def _nativepath_or_empty(path):
    if path:
        path = prim.nativepath(path)
    return path


def show_info(model):
    dialog = FlowInfo(model, stub=False)
    result = dialog.exec_()
    cmds = []
    if result == QtWidgets.QDialog.Accepted:
        flow_info = dialog.get_flow_info()
        if model.is_linked:
            # Handle link label changes separately since they belong to a
            # different flow.
            link_label = flow_info.pop('label')
            if link_label != model.name:
                cmds.append(user_commands.EditNodeLabelCommand(
                    model, model.name, link_label))
        old_flow_info = model.get_flow_info()
        if any(old_flow_info[k] != flow_info[k] for k in flow_info):
            cmds.append(user_commands.SetFlowInfo(model, flow_info))
        libraries = dialog.get_libraries()
        pythonpaths = dialog.get_pythonpaths()
        if (libraries != model.library_paths() or
                pythonpaths != model.python_paths()):
            cmds.append(user_commands.SetFlowLibraries(
                model, libraries, pythonpaths))

        if len(cmds) > 1:
            model.undo_stack().beginMacro('Changing flow properties')
        for cmd in cmds:
            model.undo_stack().push(cmd)
        if len(cmds) > 1:
            model.undo_stack().endMacro()


def pre(text):
    return u'<pre>{}</pre>'.format(cgi.escape(text, quote=True))


class LinkInfoTab(QtWidgets.QWidget):
    def __init__(self, flow_model, stub, parent=None):
        super(LinkInfoTab, self).__init__(parent)

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)

        # Set up editable flow info.
        self._label_edit = QtWidgets.QLineEdit(flow_model.link_label)
        layout.addRow('Link label', self._label_edit)

        layout.addRow('Filename', get_label(
            _nativepath_or_empty(flow_model.root_or_linked_flow_filename)))

        if flow_model.is_linked and not flow_model.node_identifier:
            layout.addRow(
                'Path from parent flow', get_label(
                    _nativepath_or_empty(flow_model.source_uri)))
        self.setLayout(layout)

    @property
    def label(self):
        return self._label_edit.text()


class ShortTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Maximum)

    def sizeHint(self):
        size_hint = super().sizeHint()
        size_hint.setHeight(50)
        return size_hint


class TagComboBox(QtWidgets.QComboBox):
    def __init__(self, tag, tags_root, parent=None):
        self._tag_key_dict = {}
        super().__init__(parent=parent)

        def flatten(lists):
            return [i for list in lists for i in list]

        def list_tags(tags):
            if tags.term:
                return [tags]
            return [list_tags(tag) for tag in tags]

        def build_tags(path, tags):
            if tags.term:
                return '/'.join(path)
            else:
                return [build_tags(path + [tag.name], tag) for tag in tags]

        def build_tags_keys(path, tags):
            if tags.term:
                return '.'.join(path)
            else:
                return [build_tags_keys(path + [tag.key], tag) for tag in tags]

        tag_list = flatten(
            build_tags([], tags_root))

        self._tag_key_dict = dict(zip(flatten(
            build_tags_keys([], tags_root)), tag_list))

        self.addItems(tag_list)

        tag_idx = self.findText(
            self._tag_key_dict.get(tag, ''))
        self.setCurrentIndex(tag_idx)

    def value(self):
        return dict(zip(self._tag_key_dict.values(),
                        self._tag_key_dict.keys())).get(
            self.currentText(), '')


class GeneralInfoTab(QtWidgets.QWidget):
    def __init__(self, flow_model, stub, parent=None):
        super(GeneralInfoTab, self).__init__(parent)
        self._flow = flow_model

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)

        # Set up editable flow info.
        flow_info = flow_model.get_flow_info()
        if flow_model.is_linked:
            label = flow_info['source_label']
        else:
            label = flow_info['label']
        self._label_edit = QtWidgets.QLineEdit(label)
        layout.addRow('Label', self._label_edit)
        self._description_edit = ShortTextEdit()
        self._description_edit.setPlainText(flow_info['description'])
        self._description_edit.setToolTip(
            "Short description used in GUI and documentation.")
        layout.addRow('Description', self._description_edit)
        self._documentation_edit = QtWidgets.QPlainTextEdit()
        self._documentation_edit.setPlainText(flow_info['documentation'])
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self._documentation_edit.setToolTip(
            "Extended help text used in documentation.")
        layout.addRow('Documentation', self._documentation_edit)
        self._version_edit = QtWidgets.QLineEdit(flow_info['version'])
        layout.addRow('Version', self._version_edit)
        self._author_edit = QtWidgets.QLineEdit(flow_info['author'])
        layout.addRow('Author', self._author_edit)
        if flow_model.maintainer:
            self._maintainer_edit = QtWidgets.QLabel(flow_model.maintainer)
            layout.addRow('Maintainer', self._maintainer_edit)
        self._copyright_edit = QtWidgets.QLineEdit(flow_info['copyright'])
        layout.addRow('Copyright', self._copyright_edit)
        self._min_version_edit = QtWidgets.QLineEdit(flow_info['min_version'])
        self._min_version_edit.setToolTip(
            'Minimum allowed Sympathy version. For example "1.2.3". Opening '
            'the flow in earlier versions of Sympathy is still possible, '
            'but will result in a warning')
        self._min_version_validator = QtGui.QRegExpValidator(
            QtCore.QRegExp(r"[0-9]+\.[0-9]+\.[0-9]+"))
        self._min_version_edit.setValidator(self._min_version_validator)
        layout.addRow('Minimum Sympathy version', self._min_version_edit)

        self._tag_combo = TagComboBox(
            flow_info['tag'], self._flow.app_core.library_root().tags.root)
        layout.addRow('Tag', self._tag_combo)

        self._identifier_edit = QtWidgets.QLineEdit(flow_info['identifier'])
        layout.addRow('Identifier', self._identifier_edit)

        layout.addRow('Filename', get_label(
            _nativepath_or_empty(flow_model.root_or_linked_flow_filename)))

        if not _is_file_flow(flow_model):
            self._identifier_edit.setEnabled(False)
            self._tag_combo.setEnabled(False)

        self._icon_edit = PathLineEdit(
            self._flow.icon_filename,
            root_path=os.path.dirname(self._flow.root_or_linked_flow_filename),
            placeholder_text='SVG filename',
            filter='SVG icon files (*.svg);;All files (*.*)',
            default_relative=True)

        layout.addRow('Icon', self._icon_edit)

        if not self._flow.root_or_linked_flow_filename:
            self._icon_edit.setEnabled(False)

        # Show different UUIDs depending on whether subflow is linked and
        # whether we are showing stub or full flow.
        namespace_uuid, item_uuid = uuid_generator.split_uuid(
            flow_model.full_uuid)
        layout.addRow('Namespace UUID', get_label(pre(namespace_uuid)))
        if flow_model.is_linked:
            if stub:
                layout.addRow('UUID', get_label(pre(item_uuid)))
                layout.addRow(
                    'Source UUID', get_label(pre(flow_model.source_uuid)))
            else:
                if flow_model.source_uuid is not None:
                    layout.addRow('UUID', get_label(
                        pre(flow_model.source_uuid)))
        else:
            layout.addRow('UUID', get_label(pre(item_uuid)))
        layout.addRow(
            'State', get_label(pre(flow_model.state_string())))

        self.setLayout(layout)

    @property
    def label(self):
        return self._label_edit.text()

    @property
    def description(self):
        return self._description_edit.toPlainText()

    @property
    def documentation(self):
        return self._documentation_edit.toPlainText()

    @property
    def author(self):
        return self._author_edit.text()

    @property
    def version(self):
        return self._version_edit.text()

    @property
    def min_version(self):
        return self._min_version_edit.text()

    @property
    def copyright(self):
        return self._copyright_edit.text()

    @property
    def icon(self):
        return self._icon_edit.path()

    @property
    def tag(self):
        return self._tag_combo.value()

    @property
    def identifier(self):
        return self._identifier_edit.text()


def _is_file_flow(flow):
    return (flow.root_or_linked_flow_filename and
            flow.root_or_linked_flow() is flow)


class LibrariesTab(QtWidgets.QWidget):
    def __init__(self, flow_model, parent=None):
        super(LibrariesTab, self).__init__(parent)
        self._flow = flow_model
        self._library_widget = PathListWidget(
            flow_model.library_paths(),
            recent=preferences.get_recent_libs(),
            root_path=os.path.dirname(self._flow.root_or_linked_flow_filename),
            default_relative=True)
        self._pythonpaths_widget = PathListWidget(
            flow_model.python_paths(),
            root_path=os.path.dirname(self._flow.root_or_linked_flow_filename),
            default_relative=True)

        if not _is_file_flow(self._flow):
            self._library_widget.setEnabled(False)
            self._pythonpaths_widget.setEnabled(False)

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        layout.addRow('Workflow libraries', self._library_widget)
        layout.addRow('Python paths', self._pythonpaths_widget)
        self.setLayout(layout)

    @property
    def library_paths(self):
        return self._library_widget.paths()

    @property
    def recent_library_paths(self):
        return self._library_widget.recent()

    @property
    def python_paths(self):
        return self._pythonpaths_widget.paths()


class EnvironmentTab(QtWidgets.QWidget):
    root_msg = ('Note: Only the root flow and linked flows can have '
                'workflow environment variables')

    def __init__(self, flow_model, parent=None):
        super(EnvironmentTab, self).__init__(parent)
        self._flow = flow_model
        self._root = flow_model.root_or_linked_flow()
        layout = QtWidgets.QVBoxLayout()
        self._env_widget = preferences.ModifyEnvironmentWidget(self)

        if self._flow is not self._root:
            self._env_widget.setEnabled(False)
            layout.addWidget(QtWidgets.QLabel(self.root_msg))

        layout.addWidget(self._env_widget)
        self._old_env = self._flow.environment
        self._env_widget.set_variables(self._old_env)
        self.setLayout(layout)
        self._env_widget.resize_to_content()

    def apply(self):
        workflow_env_vars = self._env_widget.variables()
        if workflow_env_vars != self._old_env:
            assert self._flow is self._root, self.root_msg
            cmd = user_commands.EditWorkflowEnvironment(
                self._flow,
                workflow_env_vars,
                self._old_env)

            self._flow.undo_stack().push(cmd)


def other_info_tab(flow_model, stub):
    stacked_widget = StackedTextViews()

    full_json = pre(json.dumps(flow_model.to_dict(stub=stub), indent=2))
    stacked_widget.add_text('Full JSON', full_json)

    aggregation = pre(json.dumps(
        flow_model.aggregation_settings, indent=2))
    stacked_widget.add_text('Aggregation Settings', aggregation)

    overrides = pre(json.dumps(flow_model.override_parameters, indent=2))
    stacked_widget.add_text('Parameter Overrides', overrides)

    pretty_graph = pre(flow_model.print_graph())
    stacked_widget.add_text('Graph', pretty_graph)

    return stacked_widget


class FlowInfo(QtWidgets.QDialog):
    """Show and allow changing basic flow information."""

    def __init__(self, flow_model, stub, parent=None, flags=QtCore.Qt.Widget):
        super(FlowInfo, self).__init__(parent, flags)
        self._is_linked = flow_model.is_linked

        self.setWindowTitle(u'Properties {}'.format(
            prim.format_display_string(flow_model.name)))
        self._main_layout = QtWidgets.QVBoxLayout()

        if self._is_linked:
            self._link_info = LinkInfoTab(flow_model, stub, parent)

        self._general_info = GeneralInfoTab(flow_model, stub, parent)
        self._libraries_tab = LibrariesTab(flow_model, parent)
        self._environment_tab = EnvironmentTab(flow_model, parent)

        if flow_model.library_node:
            for tab in [self._general_info,
                        self._libraries_tab,
                        self._environment_tab]:
                tab.setEnabled(False)

        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.addTab(self._general_info, 'General')
        if self._is_linked:
            tab_widget.addTab(self._link_info, 'Link')
        tab_widget.addTab(self._libraries_tab, 'Libraries')

        tab_widget.addTab(self._environment_tab, 'Environment variables')
        tab_widget.addTab(other_info_tab(flow_model, stub), 'Advanced')

        self._main_layout.addWidget(tab_widget)
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.apply)
        button_box.rejected.connect(self.reject)
        self._main_layout.addWidget(button_box)
        self.setLayout(self._main_layout)

    def apply(self):
        self._environment_tab.apply()
        self.accept()
        preferences.set_recent_libs(
            self._libraries_tab.recent_library_paths)

    def get_flow_info(self):
        """Return a dictionary with the (possibly updated) flow info."""
        flow_info = {
            'label': self._general_info.label,
            'description': self._general_info.description,
            'documentation': self._general_info.documentation,
            'author': self._general_info.author,
            'version': self._general_info.version,
            'min_version': self._general_info.min_version,
            'copyright': self._general_info.copyright,
            'icon_filename': self._general_info.icon,
            'tag': self._general_info.tag,
            'identifier': self._general_info.identifier}
        if self._is_linked:
            flow_info.update({
                'source_label': self._general_info.label,
                'label': self._link_info.label})
        return flow_info

    def get_libraries(self):
        """Return a list with the (possibly updated) workflow libraries."""
        return self._libraries_tab.library_paths

    def get_pythonpaths(self):
        """Return a list with the (possibly updated) workflow python paths."""
        return self._libraries_tab.python_paths


class LibraryComboBox(QtWidgets.QComboBox):

    def __init__(self, paths, parent=None):
        super().__init__(parent=parent)

        platform_developer = settings.instance()['Gui/platform_developer']

        for path in paths:
            li = library_info.read_library_info(directory=path)
            ident = li['General']['identifier']
            library_path = li['General']['library_path']

            if platform_developer or ident not in (
                    Gui.library.platform_libraries()):
                self.addItem(li['General']['name'])
                i = self.count() - 1

                self.setItemData(
                    i, path, role=QtCore.Qt.ToolTipRole)
                self.setItemData(
                    i, {'id': ident, 'root_path': path,
                        'library_path': library_path},
                    role=QtCore.Qt.UserRole)

    def value(self):
        return self.itemData(self.currentIndex(), role=QtCore.Qt.UserRole)


class ChooseLibraryPage(QtWidgets.QWizardPage):
    def __init__(self, libraries, parent=None):
        super().__init__(parent=parent)
        layout = QtWidgets.QVBoxLayout()

        self._library = LibraryComboBox(libraries)
        self._library.setCurrentIndex(-1)

        layout.addWidget(self._library)

        self.setTitle('Choose Library')
        self.setLayout(layout)

    def library(self):
        return self._library.value()

    def validatePage(self):
        return self._library.currentIndex() > -1


def wizard_form_layout():
    layout = QtWidgets.QFormLayout()
    layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
    layout.setFormAlignment(QtCore.Qt.AlignLeft)
    layout.setLabelAlignment(QtCore.Qt.AlignVCenter)
    layout.setVerticalSpacing(15)
    return layout


class ChooseDetailsPage(QtWidgets.QWizardPage):

    def __init__(self, tags, parent=None):
        super().__init__(parent=parent)
        layout = wizard_form_layout()

        self._tag = TagComboBox(None, tags)
        self._identifier_re = '.*'
        self._identifier = sywidgets.ValidatedTextLineEdit()
        self._identifier.set_keep_last_valid_value(False)
        self._identifier.setBuilder(self._validate_identifier)

        layout.addRow('Tag', self._tag)
        layout.addRow('Identifier', self._identifier)

        self.setTitle('Choose Details')
        self.setLayout(layout)

    def _validate_identifier(self, text):
        library_path = self.wizard().library()['root_path']

        if self._identifier_re.match(text) is None:
            raise sywidgets.ValidationError(
                'Identifier must be dotted path of lower case segments')

        if self.wizard().flow.app_core.is_node_in_library(
                text, [library_path]):
            raise sywidgets.ValidationError(
                'Identifier must be unique in library')

        return text

    def identifier(self):
        return self._identifier.text()

    def tag(self):
        return self._tag.value()

    def initializePage(self):
        library_id = self.wizard().library()['id']
        self._identifier.setText(library_id + '.flows.')
        self._identifier_re = re.compile(
            ''.join([
                '^',
                library_id.replace('.', '\\.'),
                '\\.flows',
                '(\\.[a-z]([a-z0-9]){2,})+$']))

    def validatePage(self):
        tag_ok = self._tag.currentIndex() > -1
        ident_ok = self._identifier.valid()
        return tag_ok and ident_ok

    def details(self):
        return {
            'identifier': self._identifier.text(),
            'tag': self._tag.value(),
            'tag_text': self._tag.currentText()}


class SummaryPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = wizard_form_layout()

        self.setTitle('Summary')
        self.setLayout(layout)

        self._filename = QtWidgets.QLineEdit()
        self._tag = QtWidgets.QLineEdit()
        self._identifier = QtWidgets.QLineEdit()

        self._details = {'identifier': '', 'tag': '', 'tag_text': ''}

        self._filename.setReadOnly(True)
        self._tag.setReadOnly(True)
        self._identifier.setReadOnly(True)

        layout.addRow('Filename', self._filename)
        layout.addRow('Tag', self._tag)
        layout.addRow('Identifier', self._identifier)
        self.setLayout(layout)

    def initializePage(self):
        self._details = self.wizard().details()
        ident = self._details['identifier']
        self._library = self.wizard().library()
        root_path = self._library['root_path']
        library_path = self._library['library_path']

        seg = self._details['identifier'].split(self._library['id'] + '.')[-1]
        segs = seg.split('.')
        segs = segs[:-1] + ['flow_' + segs[-1] + '.syx']

        filename = os.path.join(*(
            [prim.nativepath_separators(p) for p in
             [root_path, library_path] + segs]))

        self._filename.setText(filename)
        self._identifier.setText(ident)
        self._tag.setText(self._details['tag_text'])

    def filename(self):
        return self._filename.text()

    def validatePage(self):
        return True


class SaveSubflowAsNodeWizard(QtWidgets.QWizard):
    def __init__(self, flow_, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Configure project environment')
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        # On Windows the Wizard shows the WindowTitle in the wrong
        # place if we use the native style
        self.setWizardStyle(QtWidgets.QWizard.ClassicStyle)

        self.flow = flow_
        tags = flow_.app_core.library_root().tags.root

        library_paths = util.library_paths(flow=flow_)
        self._library_page = ChooseLibraryPage(library_paths)
        self._details_page = ChooseDetailsPage(tags)
        self._summary_page = SummaryPage()

        self.addPage(self._library_page)
        self.addPage(self._details_page)
        self.addPage(self._summary_page)

    def library(self):
        return self._library_page.library()

    def details(self):
        return self._details_page.details()

    def filename(self):
        return self._summary_page.filename()
