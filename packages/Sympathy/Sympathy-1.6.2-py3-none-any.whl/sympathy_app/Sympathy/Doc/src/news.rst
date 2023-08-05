.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2010-2017 Combine Control Systems AB
..
..     Sympathy for Data is free software: you can redistribute it and/or modify
..     it under the terms of the GNU General Public License as published by
..     the Free Software Foundation, either version 3 of the License, or
..     (at your option) any later version.
..
..     Sympathy for Data is distributed in the hope that it will be useful,
..     but WITHOUT ANY WARRANTY; without even the implied warranty of
..     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
..     GNU General Public License for more details.
..     You should have received a copy of the GNU General Public License
..     along with Sympathy for Data. If not, see <http://www.gnu.org/licenses/>.

What's new
==========


News in 1.6.2
-------------


License change
^^^^^^^^^^^^^^

* Changed copyright from SysESS to Combine.

Platform changes
^^^^^^^^^^^^^^^^
* Instant warning and notice messages from nodes.
* Issue reporting, see :ref:`issues`.
* Collection of anonymous user statistics. See :ref:`privacynotice` for more
  details about privacy and data collection in Sympathy.
* Fix issues with the histogram plot in table viewer.
* Sympathy can now generate file associations and desktop entries on Linux.
* Support for spyder, if installed in the same python environment.
* Improved performance when working with large number of files.
* New options to clean up temporary files when closing flows and the
  application.
* Configuration ports can have any types.
* Built in support for creating parameter bindings to configuration ports with
  table data.
* Ability to override temp location using environment variables. See
  :ref:`env_vars`.

User interface
^^^^^^^^^^^^^^

* You can now close flows by clicking the middle mouse button on the respective
  tab.
* Wizard configuration can now be maximized.
* Changed menus for creating and removing ports.
* New text editor with search support, used for json and text viewers.
* Restructured command line arguments:

  * Help texts should be more consistent.
  * New options for generating documentation.

* Improved feedback when:

  * Library package fails to load.
  * Some types of corrupt flows are loaded.

* New context menu option to create library node from subflow.

Node changes
^^^^^^^^^^^^

* Using combo-boxes for choice parameters with single selection.

* New simplified wizards for some plot types in figure node.
* Improved the ability of
  :ref:`org.sysess.sympathy.visualize.figurecompressorgui` and
  :ref:`org.sysess.sympathy.visualize.figuresubplot` to reproduce their input
  figures:

  * Improved getting labels from legends.
  * Correctly reproduce custom tick labels.
  * Support for reproducing box plots, rectangles, ellipses, and error bars.
  * Support for reproducing QuadMesh artist (from matplotlib's pcolormesh
    function).
  * Improved error messages when some features could not be reproduced.

* New option for sharing axes in
  :ref:`org.sysess.sympathy.visualize.figuresubplot`.
* :ref:`org.sysess.sympathy.visualize.figure` features:

  * Add edge color and line width properties to scatter plot.
  * Fix edit issues on MacOS.
  * Hiding the labels of a pie chart no longer hides its percentages.
  * New completions interface.

* Fixes in :ref:`DataImportCSV`:

  * Add support for a few more obscure line endings (e.g. \r).
  * Fix regression in handling of incomplete csv-files.

* :ref:`org.sysess.sympathy.data.table.calculatorgeneric`:

  * Improved performance of local_min/local_max.
  * Fix a problem with masked values not being treated correctly in
    local_min/local_max.
  * Removed unnecessary warnings.
  * Empty calculations are now allowed and do nothing.

* :ref:`org.sysess.sympathy.datasources.filedatasource`: Paths can be relative
  to library directory.

* :ref:`org.sysess.sympathy.create.createtable`:

  * Can now paste multiple values.
  * Always shows float values in C locale.

* :ref:`org.sysess.sympathy.machinelearning.export`: added datasource output.
* :ref:`org.sysess.sympathy.datasources.filedatasourcemultiple`: can search for
  files, directories or both.
* :ref:`org.sysess.sympathy.data.table.dropnantable`: able to choose columns.
* :ref:`org.sysess.sympathy.data.table.assertequaltable`: can add more ports.
* :ref:`org.sysess.sympathy.filters.columnfilternode`: standardized
  configuration GUI.
* :ref:`org.sysess.sympathy.data.table.holdvaluetable`: able to choose columns.
* :ref:`org.sysess.sympathy.create.configureparameters`: list choices and
  editors updated from data.


New nodes
^^^^^^^^^

* :ref:`org.sysess.sympathy.texts.splittext`
* :ref:`org.sysess.sympathy.data.table.unpivottablenode` and list version.
* :ref:`org.sysess.sympathy.setcolumnnamesintablewithtable` and list version.

* List versions of several existing nodes:

 * :ref:`org.sysess.sympathy.json.jsonstolists`
 * :ref:`org.sysess.sympathy.json.jsonstodicts`
 * :ref:`org.sysess.sympathy.data.text.tables2texts`
 * :ref:`org.sysess.sympathy.convert.textstojsons`
 * :ref:`org.sysess.sympathy.texts.concatenatetextslist`

Documentation
^^^^^^^^^^^^^

* Documentation is built as part of the installation process.  This means
  that documenatation should usually be available directly after
  installation.
* Third-party library documentations can be built separately.
* Documentation is now by default built for only the platform and the
  standard library.
* Documentation pages are generated for library subflows. The subflows
  documentation can be edited in the subflow properties dialog.
* Building the documentation places it in <SY_ROOT>/Docs/ by default.
* Node documentation pages now start with the node's description.
* A warning is automatically added if a node is deprecated.

* Nodes can now have a list of related nodes, which shows up on the node's
  documentation page.
* A node's docstring is now used as description if the description field is
  missing or empty.
* Basic node documentation for nodes with optional ports.
* Updated documentation for available command line arguments.

API changes
^^^^^^^^^^^

* More guards against using bad arguments in table and adaf. For example, use
  of reserved names. Recarrays in place of numpy arrays, etc.
* Datetime parameter can set editor display format to show only date and allows
  fractional second precision.
* Expanded names API with another parameter: fields.

  * Added col_paths as a new kind of names field for accessing data.

* Added new completions API.

Python versions
^^^^^^^^^^^^^^^

* Compatibility with Python 3.7.3 in virtualenv.
* Compatibility with h5py >=2.10 and dask>=2.
* Compatibility with scikit-learn >= 0.19.2.
* Compatibility with networkx >= 2.4.


News in 1.6.1
-------------
Release 1.6.1 is a bug-fix release addressing several bugs present in 1.6.0.

Platform changes
^^^^^^^^^^^^^^^^
* Write value and list to the syx file again for ParameterList. This change will
  have to wait until we have rooted out all nodes that use .value or .list of a
  list parameter.
* Made it possible to open workflow with reference to missing library.
* Made it possible to open tabbed subflow configurations containing failed
  configurations.

Node changes
^^^^^^^^^^^^
* Changes in :ref:`org.sysess.sympathy.visualize.figure`:

  * Add property 'Distance to Axes' to legend. Use this to tweak the position of
    the legend when placed outside of the Axes. If the legend is placed inside the
    Axes this property is ignored.
  * Avoid rare exception when editing some properties.
  * Improved default values and editors for Annotations.

* Changes in :ref:`org.sysess.sympathy.visualize.figurecompressorgui` and
  :ref:`org.sysess.sympathy.visualize.figuresubplot`:

  * Fixed a bug when copying axes with unsupported elements. Those elements will
    now simply be ignored.
  * Fix colorbar handling.

* Fixed python 3 incompatibility in
  :ref:`org.sysess.sympathy.machinelearning.export`.
* Fixed inability to configure and execute Calculator Table(s) if comment
  contained newlines.
* Introduced compatibility option for
  :ref:`Select rows in Table(s)<org.sysess.sympathy.data.table.selecttablerows>`.

* Fixed issues with configuration related to missing list and value in:

  * :ref:`org.sysess.sympathy.data.table.indextable`
  * :ref:`org.sysess.sympathy.data.adaf.adaf2table`
  * :ref:`org.sysess.sympathy.list.filterlisttable`

* Fixed issues with preview/viewer on Windows for:

  * :ref:`org.sysess.sympathy.html.report`
  * :ref:`org.sysess.sympathy.html.dicttogeojson`

* Fixed issue in :ref:`org.sysess.sympathy.data.json.jsontotable`.
* Fixed use of Fit/Fit Transform with
  :ref:`org.sysess.sympathy.machinelearning.one_hot_encoder`.


News in 1.6.0
-------------


Gui changes
^^^^^^^^^^^
* Panning the flow view is now mapped to middle mouse button (scroll wheel
  click). There are also toolbar buttons for panning/selection.
* New icons from Font Awesome in toolbar, menus and context menus.
* Color theme based on the standard palette in Windows 10, is used for all OSs.
* Changed keyboard shortcuts for Zoom to selection and Zoom fit all.

* Flow Overview look and feel similar to that of Library View.

* New splash screen on startup of GUI.

* Removed redundant groupings in parameter GUIs, this makes some configuration
  GUIs more compact.
* More clear highlight of invalid parameter values, on Windows.

* Double click on node executes or does nothing, will never trigger configure.
* Plots in Table viewer shows current resampling.

* Figure viewer now supports mouse interactions for 3D axes.

* Deprecation warnings are on by default. They can be disabled by unchecking
  *Display warnings for deprecated nodes* in the *Advanced* section of
  *Preferences*.


Platform changes:
^^^^^^^^^^^^^^^^^

* Supports Python 3.6+.

* Supports PySide 2 (Qt for Python). This results in smoother rendering,
  various improvements.
* Asyncio is used in place of twisted, this will make it easier to install
  Sympathy on some OSs.
* Support for installing Sympathy in a Python virtual env, on Windows.
* Improved platform stability, undeterministic process crashes when running and
  on shutdown caused by PySide do not seem to happen anymore.
* Improved structure of menus, with new groupings and consistent ordering.
* Windows installer produces different package structure, similar to a wheel
  install.

* Added json parameter type.
* Added datetime parameter type.
* Added dict port type.
* Added Html port type.
* Added GeoJSON port type.
* Added Table editor for json parameter type.
* General preview which can easily be added to nodes.
* list_node_decorator replaces list_node_factory.

* Reduce size of syx files by not writing descriptions etc for all parameters.
  Pretty print parameter structures for increased legibility.
* Selections can be expanded while holding down Ctrl (Cmd on OSX). Ctrl + click
  toggles selection of individual nodes.

* List parameters with static lists are now automatically updated from their
  definition.
* Automatically fix minor inconsistencies between .value and .value_names during
  update_parameters. Warn about parameters that are still inconsistent during
  execute/configure.

* Documentation improvements:

  * New instructions for wheel install, now also for Windows.
    See :ref:`installation`.
  * New instructions for debugging using PyCharm. See :ref:`pycharm_debug`.
  * Show labels for parameters in node documentation.
  * Improved documentation about node libraries and their structure.

* No longer supported:

  * Python 2. Python 3.5 and older.
  * PySide.
  * Built-in debugging and editing using Spyder.
  * Built-in benchmark of the platform.

* Add maintainer information to library.ini metadata. Useful when maintainer and
  original author are not the same.
* Node copyright notice is now inherited from library.ini metadata if
  unspecified in the node. Allows less repetition when creating nodes.


Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^

* Datasource can supply URL to importer nodes.
* Support for URL datasource in import nodes and new
  :ref:`org.sysess.sympathy.files.downloadfile`.
* VJoin, Transpose: improved feedback when constructing unsupported columns
* Select columns in Table uses new preview feature.
* New :ref:`org.sysess.sympathy.visualize.figure`:

  * Many different improvements to the configuration gui and to the code.
  * Allow setting major/minor ticks.
  * Support for legend outside of axes.
  * Enabling and disabling individual plots.
  * Uses new preview.
  * The node no longer outputs its configuration in the form of a Table.
  * Improved support for plotting datetimes
  * Improved documentation.

* The old figure node can still be used, but will be deprecated at some point
  in the near future.

* Transpose can set column names even when there are no rows
* Consistently using "regex" to refer to regular expressions in node configurations.
* Calculator should be able to detect res-dependencies that use other quoting than ''.
* Improved reading of typed input value:

  * Mask nodes.
  * Replace value in Table
  * Select rows in Table

* :ref:`F(x)<org.sysess.sympathy.data.fx>` can be configured without external file.

New nodes/plugins:
^^^^^^^^^^^^^^^^^^

* :ref:`org.sysess.sympathy.html.report`
* :ref:`org.sysess.sympathy.html.dicttogeojson`
* :ref:`org.sysess.sympathy.html.htmltotext`

* :ref:`org.sysess.sympathy.datasources.renames`
* :ref:`org.sysess.sympathy.files.downloadfile`

* :ref:`org.sysess.sympathy.data.json.selectkeyjson`
* :ref:`org.sysess.sympathy.data.json.removekeyjson`
* :ref:`org.sysess.sympathy.data.json.splitonkeyjson`

* :ref:`org.sysess.sympathy.dict.insert`
* :ref:`org.sysess.sympathy.dict.update`
* :ref:`org.sysess.sympathy.dict.getitem`
* :ref:`org.sysess.sympathy.dict.fromitems`
* :ref:`org.sysess.sympathy.dict.values`
* :ref:`org.sysess.sympathy.dict.keys`
* :ref:`org.sysess.sympathy.dict.items`

* :ref:`org.sysess.sympathy.json.jsontodict`
* :ref:`org.sysess.sympathy.json.dicttojson`
* :ref:`org.sysess.sympathy.json.jsontolist`
* :ref:`org.sysess.sympathy.json.listtojson`

Removed nodes:
^^^^^^^^^^^^^^

* Propagate Input
* Repeat Item to List
* Elementwise ADAFs to Tables
* Filter Image (deprecated)

Deprecated  nodes/plugins:
^^^^^^^^^^^^^^^^^^^^^^^^^^

* Convert specific columns in Table(s)
* Copy files with Datasources
* Rename file(s)
* Rename Files with Table
* Jinja2 Template (deprecated)
* Plot Table(s)
* Export Figures with Datasources
* Matlab Calculator

* DIVA import plugin
* LAA import plugin

API changes:
^^^^^^^^^^^^

* sympathy.api.dtypes includes handling for reading typed values from text
  input
* Deprecated ManagedNode base class.
* Removed deprecated methods from table, adaf, table_wrapper and adaf_wrapper.
* New (compatible) format for F(x) script, see :ref:`F(x)<org.sysess.sympathy.data.fx>`.
* Deprecate support for ${signal0} syntax in calculator plugins.
* Deprecate imports() from calculator plugins.


News in 1.5.3
-------------

Platform changes:
^^^^^^^^^^^^^^^^^
* Improved behavior of locked subflows:

  * Child nodes that have finished executing will give feedback immediately
    instead of after the whole locked flow has completed.
  * Child nodes that has executed successfully, in memory, will show up in
    purple color to indicate that their output port data is unavailable.
  * Output from locked child nodes will be shown like for other nodes, in the
    Messages view.
  * Modifying locked flows will no longer reload all nodes.
  * Showing progress from child nodes.

* Locked subflows and lambdas (Apply, Map) will continue executing as much
  as possible instead of aborting after the first node has failed.
* Subflow configuration wizard copes with nodes executed in locked subflows
  and executes them when needed to ensure that progress can be made.

* Toggle-able filter for list parameters with mode selection saves vertical
  space.
* Included brief description of current node state in tooltips.

* Documentation improvements:

  * Links to example flows in the node documentation for many nodes, see
    :ref:`example_flows`.
  * Documented how to create custom library tags for third party libraries, see
    :ref:`library_tags`.
  * Documented how to create plugins for calculators, importer and exporter
    nodes, see :ref:`pluginwriting`.
  * Improved documentation for Tables with more modern APIs and descriptions of
    attributes etc.

* Windows installer generates links and file associations that ignore local user
  site - this makes the bundled Python more stand-alone and helps avoid issues
  in case of package conflicts.


Figure and plotting updates:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Figure(s) can now take any sympathy object or lists of object instead of just
  tables. The configuration output table is now optional and need to be added
  explicitly to be used. Arguments can now be accessed using "arg" instead of
  "table" in expressions, eg. arg['X'] gives column X if the argument is a
  table.

* Improved the Figure node with new plot types and drawing primitives:

  * Boxplots calculating and visualizing median, average, quantiles and outliers.
  * Pie-charts.
  * Timeline plots for drawing events or states.
  * Sets of unconnected lines based on starting/ending XY points.
  * Rectangles and Ellipses.
  * Text and arrows (annotations) to point out or label parts of data.
  * Images (using the generic Figure inputs).

* Added extended example "Figure Gallery" with 12 plots to show how
  the new plot types and options can be used.

* Added options for drawing error-bars on scatter-plots and
  bar-plots.

* Frames and axes can now toggle visibility and the XY spines of the
  axes can be drawn at a predetermined XY data coordinate (eg. with
  the axis through origo), or at a given point on the screen
  (eg. center).

* Fixed bug showing tooltips for plot parameters.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Added error strategies to :ref:`org.sysess.sympathy.list.getitemlist`, when
  the list is empty.

* Add different strategies for handling lists of different lengths in
  :ref:`org.sysess.sympathy.tuple.ziptuple2`.

* Added median filtering to :ref:`Overlay Images` and :ref:`Overlay Images List`

* Added :ref:`Colormap lookup` to explicitly create colors from
  values, useful when creating many figures where exact control of the
  colors are needed. New color-maps added for discrete categories of
  objects.

* Fixed bug in :ref:`Image to List` missing one of the extracted objects.

* Improved :ref:`Generic Calculator<Calculator>` with:

  * More robust handling of dependencies between calculations.
  * Compacted layout with a larger portion available for preview.
    Input signals are shown in in the tree where functions
    are shown.
  * Drag and drop of calculations.
  * Ability to set custom attributes for each calculation.

* Error handling for :ref:`Extract lambda nodes<Extract lambdas>` with choice
  between skip and error.

* :ref:`Match Tables Nodes<org.sysess.sympathy.data.table.matchtwotables>`:
  support for masked arrays.
* :ref:`Filter ADAFs`: will only auto-refresh when it has been enabled.
* :ref:`Adaf(s) to Table(s)<org.sysess.sympathy.data.adaf.adaf2table>`:
  shows preview of available signals.
* Many nodes have toggle-able filter for their column selection editors.
* :ref:`org.sysess.sympathy.examples.daskvisualize`: improved detection
  of Graphviz installation.
* :ref:`org.sysess.sympathy.data.table.ensuretablecolumns`: can create
  type-dependent zero elements for missing columns.
* MDF importer plugin has better support for reading partially unsupported
  or broken files.
* Avoid infinite loop when loading scikit-learn 0.20.
* Excel importer plugin copes with date values outside of supported range by
  assigning masked values.

New nodes/plugins:
^^^^^^^^^^^^^^^^^^
* :ref:`Rename datasource with regex`: helps to simplify automatically
  creating new datasource names based on existing file names.
* ADAF importer plugin for LabVIEW TDMS files.
* :ref:`org.sysess.sympathy.list.transposelist` swaps the outer two layers of a
  nested list.
* :ref:`org.sysess.sympathy.keyvaluecalculation`: calculates simple descriptive
  statistics for all columns in a table.

API changes:
^^^^^^^^^^^^
* Generalized interface for import and export nodes and their plugins.
* Opt-in support for toggle-able filter for single-select parameters with
  combo box editors.
* Public APIs for creating importer and exporter plugins.
* Datasource: added getitem. Example use: ``datasource['type']``.
* Table: added setter for name. Example use: ``table.name = 'some name'``.
* New exception: SyColumnTypeError, raised when creating table columns of
  unsupported type.

News in 1.5.2
-------------

Platform changes:
^^^^^^^^^^^^^^^^^
* Fixed problem causing the OK button to be disabled (grey) when configuring
  subflows containing certain nodes (for example,
  :ref:`org.sysess.sympathy.data.adaf.interpolateadaf` and
  :ref:`org.sysess.sympathy.data.table.converttablecolumns`)
  using the Wizard or Tabbed dialog.

News in 1.5.1
-------------

Platform changes:
^^^^^^^^^^^^^^^^^
* Improved performance overhead of nodes that simply select some columns of the
  incoming data and pass them to the output.
* Significantly reduced file sizes of lambdas on disk.
* More careful disconnection of signals to improve stability and performance.
* Added option to *Unlink* linked subflows.
* Confirmation dialog when canceling subflow configurations with unsaved changes.
* Better feedback and handling of node errors when configuring subflows.
* Improved ability to open (somewhat corrupt) flows with duplicate identifiers,
  instead of failing early.
* Cleared up separation between flows linked from library and normal linked
  subflows.
* Disabled automatic documentation generation.
* Cleaned up command line options, "-" is used to separate words instead of
  "_".
* Added *Recent* libraries, to simplify switching between libraries in use.
* Restructured documentation format for Nodes.
* New installation instructions for Linux and Mac OS.
* Saving warning filter between node executions to avoid interference.
* Improved deprecation warnings for nodes, on by default.
* Fixed some regressions causing library view not to update.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Improved feedback and validation for many scalar parameters. Incorrect values
  are displayed in red and the tooltip shows why.
* Added progress and current list index, in case of error - to many list
  nodes.
* In some cases, improved performance for :ref:`Replace values in Table`.
* Improved documentation regarding handling of unmatched values for
  :ref:`Lookup Table`.
* :ref:`Select category in ADAFs` now respects the choice made in the combo box
  for raster selection.
* :ref:`Datasource` nodes store UNIX paths in their configuration, but show
  paths in native format.
* MDF Importer, improved performance when importing unsorted files and added
  option to attempt to read incomplete files without error.
* ADAF exporter, improved GUI.
* CSV exporter, improved performance.
* @ca.changed()@, @ca.changed_up()@, and @ca.changed_down()@ can now all handle
  masked arrays with scalar masks.
* Filtered several expected warnings produced by nodes.

New nodes:
^^^^^^^^^^^
* :ref:`org.sysess.sympathy.create.configureparameters`
* :ref:`org.sysess.sympathy.create.createparameters`
* :ref:`org.sysess.sympathy.data.table.createindextable`

New flows:
^^^^^^^^^^
* :ref:`org.sysess.lambda.map2flow`
* :ref:`org.sysess.lambda.map4flow`
* :ref:`org.sysess.lambda.configurablemap4flow`


News in 1.5.0
-------------
Sympathy for Data version 1.5.0 offers several improvements and new features,
such as workflows in the library and routing points for connections.

Nodes and flows from 1.3 and 1.4 should for the most part be compatible with
1.5.0.

.. * Connections are rendered as lines. This can be changed to *Spline* in
..  *Preferences -> General: connection shape* if you prefer the original look.


Platform changes:
^^^^^^^^^^^^^^^^^
* Markdown_ is now supported in text fields.
* Mark unavailable items in list views.
* list views and combobox views can be edited when customized with editor
  attribute edit=True. This makes it possible to create selections that
  includes columns that do not exist in the input data or without executing
  previous nodes.
* Shorter tab labels for flows, only showing parent flow names as necessary.
* Only nodes that are in the current libraries can be used. Current libraries
  depend on the configured libraries for the current flow and the global
  selection from preferences.
* Allow subflows to specify custom svg icons.
* Route points for connections, see :ref:`route_points`.
* 0 based indexing is used more consistently, that is, 0 is the index of the
  first element, etc. This behavior is more consistent with python code.
* English/US locale is used regardless of the host language settings.
* Generalized text-output port on all nodes.
* Flows can be added to library, see :ref:`flows_in_library`.

.. _Markdown: http://daringfireball.com/projects/markdown

API changes:
^^^^^^^^^^^^
* Improved backwards compatibility of ParameterLists during execution.
* ParameterLists return copies of its internal state disallowing direct
  mutation.
* Ability to get and set dask arrays in adaf and table APIs.
  See example nodes: :ref:`Dask max example`, :ref:`Dask stack example` and
  :ref:`Dask tail example`.
* Made getitem, setitem usable as a shorthand way of working with arrays
  columns in tables. For example table1['x'] = table2['y'].

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Improved masked arrays support in input data to
  :ref:`Select rows nodes<Select rows in Table>`.
* Custom filter predicates in
  :ref:`Select rows in Table(s)<Select rows in Table>` get normal numpy arrays
  instead of pandas Series.
* :ref:`Select rows in Table with Table` understands literal comparison
  operators such as '==' or '>' in addition to their old text representations.
* :ref:`HJoin Tables` gives consistent names when renaming duplicate columns
* :ref:`Figure` allows you to rotate bin labels in bar plots.
* New parameter in :ref:`Select rows with Table(s)<Select rows in Table>`
  turning on/off evaluation of value column. Defaults to no evaluation for new
  nodes.

New nodes:
^^^^^^^^^^
* :ref:`Mask values in Table`
* :ref:`Fill masked values in Table`
* :ref:`Drop masked values in Table`

New flows:
^^^^^^^^^^

* :ref:`org.sysess.list.append.flow`


Removed nodes:
^^^^^^^^^^^^^^
* Many deprecated nodes were removed, see :ref:`deprecations`.


News in 1.4.5
-------------

Platform changes:
^^^^^^^^^^^^^^^^^
* Fixed problem inserting linked subflow.
* Minor documentation fixes.
* Fixed default editor for list parameters.
* Improved backwards compatibility for empty selection in list parameters.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Fixed empty handling of :ref:`Filter rows in Tables`.


News in 1.4.4
-------------

Platform changes:
^^^^^^^^^^^^^^^^^
* Add default workflow environment variable SY_PARENT_FLOW_FILEPATH.
* Always show empty item in comboboxes when no selection has been made.
* Confirmation dialog when canceling node configurations with unsaved changes is
  no longer experimental and is on by default.
* More operations, such as, edit are available for locked subflows.
* Locked subflows are now available under Execution Mode.
* Limit the number of characters written to Messages window, this improves
  performance. Default setting of 32000 characters can be changed in
  Preferences -> Advanced.
* Setting to change the behaviour of moving views has been added in
  Preferences -> General.
* Reload library updates nodes that were previously missing in library.
* Running nodes can now be deleted.
* Improved font and icon rendering on high-dpi Windows 8, 10.
* Searchable text fields in Flow overview.
* New option to enable/disable window docking in General pane.
* Textfields can be manually ordered to choose how they overlap.

New nodes:
^^^^^^^^^^
* :ref:`Update Configuration with Table`: updates a node
  configuration using a table. This can be used to set almost any
  configuration option programmatically.
* Image filtering algorithms have been split from the
  ``Filter Image (deprecated)`` into the more specific nodes
  :ref:`Edge detection`, :ref:`Corner detection`,
  :ref:`Morphology (single input)`, :ref:`Transform image`,
  :ref:`Threshold image`, :ref:`Color space conversion`,
  :ref:`Color range conversion`, and :ref:`Filter image`.
  Additional algorithms have been added to some of these nodes.
* :ref:`Cartesian Product Table` node creating a table with all
  combinations of rows in the input tables. Useful for generating XY
  data for heatmap generation.
* :ref:`Insert List`, :ref:`Chunk List`.
* :ref:`Table to Text`.
* :ref:`Debug Import`, :ref:`Debug Export`.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* ORB feature detection algorithm now also outputs XY coordinates.
* :ref:`Jinja2 template` node now give the same context for Python expressions
  as the calculator node, as far as allowed by the Jinja2 template engine.
* Add optional Datasources port to :ref:`Export Texts`.
* Allow adding more ports to :ref:`Concatenate texts`.
* Fix bug where :ref:`Copy Files` would drop extensions if configured with a
  directory.
* ATF importer includes more attributes.
* LAA importer, support for autodetection
* Importers: better support for opening a large number of sydata files.
* :ref:`Export Tables`, ability to control filename using datasource.
* Customizable ports for :ref:`Append List` and :ref:`Bisect List`.
* Customizable port for :ref:`Propagate First Input`, deprecated
  ``Propagate Input``.
* :ref:`Calculator`, input port can be removed.
* Added support for masked arrays to :ref:`Replace Values in Tables` nodes.
* Showing progress for Map, Apply and Locked subflows.
* Calculator plugins can add their own packages via import statements.
* Export Datasources has changed name to :ref:`Archive files` and now supports
  packing and unpacking of ZIP, GZ, and TAR formats.
* Added progress to :ref:`F(x) nodes<F(x)>`,
  :ref:`Convert columns nodes<Convert columns in Table>` and
  :ref:`Predicate list nodes<Filter list predicate>`.

API changes:
^^^^^^^^^^^^
* New API for accessing worker settings: sympathy.api.nodeconfig.settings.
* Improved implementation of ``set_list()`` and the resulting ``ParameterList``
  with stricter promises. Parameters are given exactly as before during execute,
  but some nodes might need to be updated to make configuration work. Overall,
  this will make working with lists much easier.
* Allow the options in the combobox editor to be a dictionary with keys and
  display texts.
* Allow choosing the available states (abs/rel/flow etc.) in filename editors.
* Improved API for setting parameter editors: They can now be found in
  ``node.editors`` (as well as their old location) and ``.value()`` is no longer
  needed. Default to combobox editor for list parameters without an editor.
* Two new editors: ``synode.editors.multilist_editor`` and
  ``synode.editors.textarea_editor`` to :ref:`parameter_editors`.
* Allow passing controllers structure to ParameterGroup.gui() to ensure that it
  builds with the relevant controllers.
* New method: types, added to TypeAlias API.
* Added 'ts' and 'rasters' as new kinds of names from adaf to be used in adjust.
* Added ``raster`` method to :class:`adaf.TimeSeries`.


News in 1.4.3
-------------

Platform changes:
^^^^^^^^^^^^^^^^^
* Improved handling of labels for linked subflows. Changing the label of a
  linked subflow only changes the link label. The original source label can be
  seen in the subflows tooltip. Both labels can be changed individually in the
  subflow's properties.
* A little plus sign has been added to subflows with overrides.
* Fixed a problem with encoding the character sequence `]]>` when saving flows.
* Using synchronous state machine for more predictable state changes, hoping to
  avoid random problems with nodes ending up in the wrong state.
* Improved performance in some situations by validating fewer nodes.
* Added destination folder argument to documentation generation. See
  :ref:`start_options`.
* Fixed :ref:`Table viewer<data_viewer>` glob filtering.
* Added ability to generate documentation for node plugins.


Preferences changes:
^^^^^^^^^^^^^^^^^^^^
* Added option to the Advanced pane to clear cached Sympathy files
  (temporary files and generated documentation). Also an option to clear
  settings, restoring Sympathy to its orignial state. This may be used for
  debugging purposes.
* Changed the default MATLAB JRE setting to be disabled since it gives a big
  performance boost in cases when JRE is not used (which would be most of them).
  For existing installations you will have to change this manully, in the MATLAB
  pane.
* New library layout: Separated tag layout, which uses the same ordering as
  Tag layout, but separated into libraries.

API changes:
^^^^^^^^^^^^
* Added methods :meth:`RasterN.update_basis` and :meth:`RasterN.update_signal`.
* Improved performance and memory usage when running locked subflows and
  lambdas.
* Standardized ADAF attribute interfaces, based on abc.MutableMapping.
* Added include_empty=bool to combobox editors, usable for representing no
  selection.
* Added shallow=bool argument to :meth:`TypeAlias.source`. Custom types need to be
  updated, adding keyword shallow=False should be enough. Using shallow=True in
  calls to source can improve performance.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Improved path editors. For example, using the dialog to select a file will
  result in a path with the same state as was selected before the dialog.
* Optionally include index column in output from :ref:`Pivot Table`.
* Improved performance in Select columns in ADAFs in some situations.
* xls/xlsx importer plugins is better at handling columns with mixed types,
  especially integers and strings.
* xls/xlsx can import tables with missing values. Those positions in the table
  will be masked.
* Replaced :ref:`Jinja2 template` node with a new version accepting generic
  arguments, allowing for instance lists of tables or ADAFs as input to
  expression.
* Renamed node Either With Data Predicate to :ref:`Conditional Propagate`.
* Renamed Select columns in ADAF with Table to
  :ref:`Select columns in ADAF with structure Table`
* :ref:`Heatmap calculation` uses masked arrays instead of nan in its output.
* Improvements and bug fixes to the :ref:`figure nodes<Figure>`.
* A Datasource output to Scatter 3D Table has been added.
* Options for relative and absolute paths in :ref:`Datasource to Table` and
  :ref:`Table to Datasources`.
* Added support for integers and floating point values in
  :ref:`Replace values in Table`.
* :ref:`Datasource` has had its tabbed inteface replaced with a dropbox.
* When using a manual timestep in :ref:`Interpolate ADAF`, the time step is
  added to the raster's column attributes.
* Manually create Tables can now use 'nan' and '±inf' as float values.
* The node :ref:`org.sysess.sympathy.data.table.selecttablecolumnstype` has been
  added.


News in 1.4.2
-------------

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Improved performance of :ref:`Select Columns in Table` in cases when lots of
  columns are discarded.
* Added the node :ref:`Periodic Sequence Split Table` that can split up a Table
  into a Tables list where each element holds one periodic event.
* Support for creating masked values in :ref:`Lookup Table` and
  :ref:`Pivot Table`. Pivot node now works with any data type.
* Improved performance in all :ref:`Vjoin Tables`/:ref:`ADAFs<Vjoin ADAFs>`
  nodes with a single list input, in the case when the input list contains a
  single element.
* Optimization and new option for :ref:`HJoin Tables` with different number
  of rows analogous to :ref:`VJoin Tables`.
* Optional creation of masked array in :ref:`Ensure columns in Tables with Table`.
* Harmonized quoting for CSV importers and exporters.
* Chunked MDF writing to improve performance when exporting large Rasters.
* Extended :ref:`Vjoin Tables` with more options for controlling how to handle
  missing index.

Machine learning:
^^^^^^^^^^^^^^^^^
New machine learning nodes based on `scikit-learn <http://scikit-learn.org/>`_.
Features include:

* Operates on tabular (nummeric) data, texts, or images converted to tables
* Supervised learning using :ref:`Multi-Layer Perceptron Classifier` neural
  networks, :ref:`Support Vector Classifier`, :ref:`Logistic Regression`,
  :ref:`Decision Tree Classifier` and :ref:`Random Forest Classifier`.
* Regression using :ref:`Linear Regression`, :ref:`Kernel Ridge
  Regression`, and :ref:`Epsilon Support Vector Regression`.
* Clustering using :ref:`K-means Clustering`
* Exporting/importing trained models, extracting and visualising attributes
* Many preprocessing models including nodes such as :ref:`Normalizer`,
  :ref:`Robust Scaler`, :ref:`Label Binarizer`, :ref:`Principal
  Component Analysis (PCA)`, :ref:`Polynomial Features`.
* Combining models in a chain using :ref:`Pipeline` nodes
* Creating ensembles from models using :ref:`Voting Classifier` nodes
* Hyper parameter search using :ref:`Grid Parameter Search` or simple
  :ref:`Randomized Parameter Search`.
* Various cross-validation schemes
* Model metrics such as ROC-curves, :ref:`Confusion Matrix`, or :ref:`Learning Curve` nodes.

See also the machine learning examples from the install path of the Sympathy node library.

Platform:
^^^^^^^^^
* It is now possible to enter a minimum version for a workflow, in flow
  properties. Bear in mind that this feature is not very useful until it has
  existed for a few versions.
* Possibility to jump from an error message to the node/flow that caused the
  error.
* Some default workflow variables have been removed. Only SY_FLOW_FILEPATH and
  SY_FLOW_DIR remain.
* Lambdas can be configured to show input ports that can be used to perform
  configuration against data. See :ref:`lambda_function`.
* Improved performance of the Figure type in some situations.
* Redesigned sympathy.api.dtypes, this API should be stable.
* Configurable node ports can now be added and removed when the nodes are
  connected. See :ref:`node_section_ports`.
* Made it possible to build GUI:s from group parameters which includes children.
* Improved handling of flows and libraries in non-ascii paths.
* Reduced the maximum number of worker processes, used by default, to 4.



News in 1.4.1
-------------

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Select columns in Table(s) uses new multiselect editor mode to offer more
  options when it comes to unknown signals.
* Added new Convert columns in Table(s) nodes, old ones were renamed to Convert
  specific columns in Table(s).  New ones use multiselect editor mode to offer
  more options when it comes to unknown signals.
* Added som new nodes for manipulating files: copying, deleting, renaming,
  and moving files.
* Added node for getting table names, :ref:`Get Table Name`.
* Added node for creating json, :ref:`Manually Create JSON`.
* Added nodes for converting json, :ref:`Text to JSON` and :ref:`JSON to Text`.
* Several improvements for :ref:`Manually Create Table`. It now allows you to
  create masked arrays, floating point numbers with arbitrary precision and more
  relaxed syntax, and date time columns. It also has a new undo functionality
  which allows you to undo mistakes while editing a table.
* All functions supplied by the :ref:`Calculator<Calculator>` plugin in
  the standard library can now handle masked array.
* Improved performance of :ref:`Interpolate ADAF(s)<Interpolate ADAF>` when
  several signals from the same raster are resampled. For a file with 1000
  resampled columns the new implementation was about three times faster.
* Added option to export just the time basis in :ref:`Interpolate ADAFs`.
* Add variable 'arg' for :ref:`Jinja2 template` allowing iterating over full table.
* :ref:`F(x)` nodes now correctly produce errors for some cases where they previously
  executed, but ignored the entire source file.
* MDF importer handles rasters with a basis and no timeseries.
* :ref:`HJoin ADAFs` now has an option to merge rasters with the same name
  in systems with the same name.
* Added option to :ref:`Sort Columns in Table` to select sort order.
* :ref:`Generic Calculator<Calculator>` nodes have been added, which can
  take any type as input.

Image processing:
^^^^^^^^^^^^^^^^^
New image processing nodes based on `scikit-image <http://scikit-image.org/>`_
for automated image analysis, features include:

* Images as a new Sympathy datatype with custom image viewers. Support
  for alpha channel and any number of colour channels.
* >50 algorithms for :ref:`Filter Image`, :ref:`Morphological Image Operations`
  or :ref:`Extract Image Data`. Includes edge/corner detection, hough transforms,
  feature detection, adaptive thresholding, morphology, blob
  detection, labeling, and many more algorithms.
* Extracting :ref:`Image Statistics` and features/lines into Sympathy
  tables for further processing of results.
* Visualization by :ref:`Draw on Image` for displaying identified objects or
  features. :ref:`Overlay Images` using image layer operations.

Platform:
^^^^^^^^^
* Configurable number of node ports (select nodes). See :ref:`custom_ports`.
* Ability to modify configuration using an optional json configuration port
  available to any node. See :ref:`configuration_port`.
* New method: ParameterList.selected_names (usable with multiselect editor).
* Changes to ParameterEditorListWidget in multiselect: moved selection buttons
  to context menu. Context menu is always available.
* New boolean option: mode, for multiselect editor which adds choice of how to
  interpret the selection in selected_names.
* New api function: nodeconfig.adjust, useful for implementing
  adjust_parameters.
* New typealias method: names, useful for implementing adjust_parameters and
  as a common way of accessing names of different kind.
* Extended output of profiling, with graphs of nodes and flows if Graphviz is
  available. See :ref:`profiling`.
* Changed and documented API for creating new types. See :ref:`create_type`.
* Improved performance when working lists or tuples of figures.
* Improved performance of some operations like reloading and unlinking subflows.
* More extensive linking of propagated data that has not been accessed. This
  greatly improves performance of nodes that operate on the outer container
  when working with composite elements. For example, `Item to List` with
  `Random ADAFs` as input.
* Subflow progress overlay has been improved and stays visible while
  nodes are executing. Completion of nodes affect the progress meter
  and Locked subflows and Lambdas are counted as 1 node.
* Improved presentation of node errors when running sympathy in CLI mode.
* Copying subflows with parameter overrides is more reliable.



News in 1.4.0
-------------
Sympathy for Data version 1.4.0 offers support for Python 3, improved
responsiveness and several new features such a Flow overview window, a popup
dialog for adding nodes and an improved library filter with highlighting of
matches.

Many small improvements were made to the standard node library, for example,
exporter plugins preview the filenames automatically.

Nodes and flows from 1.3.0 should be compatible with 1.4.0.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* "Table Search and Replace" has been replaced with
  :ref:`Replace values in Table with Table`.
* Old Matlab nodes have been replaced with new ones, which are using the new
  :ref:`MATLAB API<matlabapi>`.
* A bug which prevented all markers being used in the Figure nodes has been
  resolved.
* :ref:`TimeSync ADAF` can now use both integer and float time bases and
  propagates basis unit.
* :ref:`Filter ADAFs` filter column can be selected from a dropdown list
  instead of being hardcoded.
* Workflow examples have been added for (almost) all library nodes.
* Improved performance of :ref:`Interpolate ADAF(s)<Interpolate ADAF>`.
* Future imports in :ref:`Calculator` and other code input. This changes
  the meaning of the operator ``/`` to always mean "true division". To get
  floor division use the operator ``//``. Literal strings will also be
  interpreted differently. The syntax ``'text'`` will now produce a text object
  (``str`` in python 3, ``unicode`` in python 2). Use the syntax ``b'binary'``
  to produce a binary object (``bytes`` in python 3, ``str`` in python 2).
* Preview button have been removed and preview handling have been updated for
  all export/import nodes.
* Node :ref:`Export Texts` can now use dynamic file extensions.
* Many obsolete nodes have been deprecated and are due for removal in the next
  major version, 1.5.0. To see if your flows contain any of these nodes, go to
  File/Preferences/Advanced and check 'Display a warning when running
  deprecated nodes', and run your flows. You can then use the new Flow overview
  to find these nodes.
* :ref:`TimeSync ADAFs` now correctly saves column attributes for the raster
  column.
* :ref:`Set column attributes in Table(s)<Set column attributes in Table>` can
  remove attributes.
* Icons for all standard library nodes previously missing an icon. Default icon
  has been updated.

Platform:
^^^^^^^^^
* Support for running Sympathy under `Python <https://www.python.org/>`_ 3. The
  platform and nodes from the standard library should work well under
  Python 3. Third party libraries written for Python 2 will probably need to be
  upgraded to run on Python 3. See :ref:`python3`.
* Synchronous task handling based on Twisted instead of ZeroMQ. This should
  reduce delay when executing and make the GUIs more responsive overall while
  lowering the load on your system.
* Automatic viewer reload when nodes are executed.
* Improved handling of node states.
  For example, if a node produces an error all following nodes will be clearly
  marked as not executable.
* Significant GUI speedups when working with large flows with many subflows.
* Improved :ref:`library view<node_library_window>` with a new search
  algorithm which gives better, more focused search results, and an advanced
  search and search highlighting.
* Add nodes by starting a connection and dropping it on an empty part of the
  flow. This opens a popup which allows to quickly search and insert a new node
  from the library. The shortcut ``Ctrl+Shift+N`` also opens the same popup at
  the current mouse position.
* Flow overview showing all subflows and nodes, and the ability to search for
  nodes within flows (including subflows and linked flows). Click a node or
  subflow to go directly to that node or subflow. See :ref:`flow_overview` for
  more details.
* Button in the data viewer for jumping to a specific row. When data is
  transposed this will scroll the view horizontally instead of vertically.
* Improved layering of nodes so that selected and moved nodes
  always end up on top.
* :ref:`MATLAB API<matlabapi>` introduced, with Table-like functions,
  which is much simpler to use.
* The old MATLAB API has been removed.
* Flow environment variables are now added by right clicking in a flow,
  clicking Properties, and then going to the Environment variables tab.
  This was previously done in Preferences.
* Added a small example on how to use environment variables for CLI execution.
* Viewers show the node icon and the name indicates which node/port that
  is shown.



News in 1.3.5
-------------

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* Calculations in :ref:`Calculator` can be deselected for output
  enabling better support for intermediary calculations. This also enables
  intermediary calculations to have different lengths from output columns.
* The input table(s) in :ref:`Calculator` can be easily copied over to
  the output table(s) with the new *Copy Input* parameter. Calculations with
  the same column name override columns from the input table(s).
* :ref:`MATLAB nodes<Matlab Tables>` and :ref:`Matlab Calculator` have gotten
  better cross-platform compatibility.
* :ref:`Matlab Calculator` has been updated with the same GUI and (almost) the
  same functionality as :ref:`Calculator List`.
* :ref:`Matlab Table` and :ref:`Matlab Tables` have gotten a new simplified
  format. See the documentation for details on how to use that. This format can
  also be imported and exported in :ref:`Table` and :ref:`Export Tables`
  respectively. A Table-like API is planned for a future release. The API that
  currently resides in Sympathy/Matlab will also be deprecated in a later
  release, in favor of the new format. The old nodes are left for
  compatibility, so current flows and scripts will still work.
* The generic :ref:`Empty` node allows to specify the data type of the output
  port. The previous, specific, Empty-nodes have been deprecated.
* :ref:`Rename column nodes<Rename columns in Table>` have more consistent
  priority rules when more that one column are renamed to the same name.
* :ref:`Extract lambda nodes<Extract lambdas>` are more robust with regard to
  corrupt flows. One corrupt flow should no longer stop the nodes from
  extracting other lambdas.
* New node: :ref:`Heatmap calculation` useful for feeding the heatmap in
  :ref:`Figure(s) from Table(s)<Figure>`.
* New features for heatmaps in :ref:`Figure(s) from Table(s)<Figure>`:
  logarithmic color scales and Z labels.
* :ref:`Datasource` and other nodes where you specify a file path can specify
  paths relative to its own workflow or the top workflow. This can make a
  difference when working with linked subflows.
* :ref:`org.sysess.sympathy.datasources.filedatasourcemultiple` GUI is no longer
  slowed down when searching large folder structures. If the search takes to
  long it is aborted, and to get the full results the node has to be executed.
* The table name used for the output in :ref:`HJoin Table` can now be selected.
* Fixes to extract flows as lambdas so that workflow environment variables and
  flow name are set correctly.
* :ref:`Timesync ADAFs` can now use integer timebases and correctly displays
  datetimes in the plot.
* :ref:`Assert equal table` now treats NaNs as equal.
* Improved config gui and handling of NaN values, masked values and non-ascii
  binary data in :ref:`VSplit Table(s)<VSplit Table>`.
* A new node has been added :ref:`HJoin ADAFs pairwise`.
* When zooming and panning in :ref:`Plot Table` and using datetime as X axis,
  the current time span in the plot is displayed.
* SQL importer plugin can use SQLAlchemy and provide betters autodetection of
  existing tables.
* SQL exporter plugin can use SQLAlchemy.
* Improved documentation generation with support for libraries on different
  drives or on unicode paths.

Platform:
^^^^^^^^^
* Nodes have gotten dynamic port icons that display the actual types.
* Color of textfields can now be changed.
* A textfields can be moved by dragging on any part of it. It is now edited by
  double clicking it or by right clicking and choosing "Edit".
* The table viewer and any viewer which uses that component (i.e. ADAF viewer)
  can now be transposed for better viewing of long column names and tables with
  few rows but many columns.
* Table viewer now supports copying values and/or column names as a table or as
  text.
* The viewer can now show histograms for more types of data.
* Allow maximizing subflow configurations.
* Linked flows can now be placed on a different drive than their parent flows.
* combo_editor for string parameters can now have an empty list of options.
* Invalid subflows are more reliably shown as invalid (gray). Now any subflow
  which looks executable should be executable.
* Subflows show an error indicator if they contain any nodes that are not found
  in the node library. This should make such nodes much easier to find.
* Better feedback when trying to open a non-existing or corrupt workflow.
* The platform can handle a larger number of linked files without running into
  the OS limit.
* An Advanced tab has been added to Preferences, with one option to limit the
  number of concurrent nodes that may be executed, and one option to display
  warnings about deprecated nodes.
* New preference option to set number of concurrent worker processes. This may
  help with performance for heavily branched flows.
* Python 3 support for files created with the node and function wizards.
* Library wizard can create subdirectories.
* Spyder can't handle files on file paths contaning non-ascii characters, and
  will fail to start when trying to debug nodes. An error message is now
  displayed to notify the user of this.
* Improved stability of type inference.
* File datasources always store absolute paths.
* Database datasources can use SQLalchemy in addition to ODBC.



News in 1.3.4
-------------
Sympathy for Data version 1.3.4 offers improvements to existing nodes,
including several new plot types for the figure nodes and overall polish.

Node/plugin changes:
^^^^^^^^^^^^^^^^^^^^
* :ref:`Figure nodes<Figure>` have been massively improved with
  several new plot types (scatter/bar plots/histograms/heatmaps), improved gui,
  etc
* Extended :ref:`figure export node<Export Figures>` with plugin exporter
  structure as for other types and choice of specifying image size in mm and
  dpi
* :ref:`Reporting Nodes<lib_reporting>` have been improved with rulers in
  layout window, pdf exporting and auto creation of tree structures
* :ref:`Calculator<Calculator>`, allows accessing the input table
  directly under the name "table" allowing for a way to test if a column
  exists. The node was also extended with the json module in the execution
  context
* ca.changed now correctly returns empty array for empty input
* Added functions ca.global_min and ca.global_max to standard calculator
  plugin. These handle empty input as you would expect
* :ref:`Interpolate ADAF` nodes have improved handling of missing values and
  resampling of zero-length signals
* :ref:`Datasource` and :ref:`exporter<Export Tables>`/:ref:`importer<Table>`
  of SQL can use SQLAlchemy
* :ref:`Pad List` input can be different types of lists
* :ref:`Predicate<Filter list predicate>` nodes have new editors for writing
  code
* :ref:`VJoin<VJoin Table>` nodes can mask missing values
* MDF importer creates MDF_datetime metadata
* :ref:`Assert Equal Table` allows approximate comparison of floats
* Added documentation for internal nodes (:ref:`Apply`, :ref:`Map`, etc.)

APIs:
^^^^^
* Made it possible to specify viewer and icon for custom types (TypeAlias). For
  details, see :ref:`create_type`
* Only scanning Libraries for plugins, PYTHONPATH is no longer included
* Scalar parameters can use the new combobox editor. See
  :ref:`All parameters example` for an example
* Code parameter editor for string parameters. See :ref:`parameter_editors` for
  details and :ref:`All parameters example` for an example
* Allow :ref:`controllers` to trigger on user-specified value. For an example
  of this see :ref:`Controller example`
* Implemented ``cols()`` and added documentation for col/cols and
  Column class. See :ref:`Table API<tableapi>`
* Added ``attrs`` property to :ref:`Table API<tableapi>`
* Expose dtypes module in sympathy.api

New nodes:
^^^^^^^^^^
* :ref:`Histogram calculation`
* :ref:`Bisect list`
* :ref:`Empty`
* :ref:`Extract Flows as Lambdas`
* :ref:`Export Figures with Datasources`
* :ref:`Concatenate texts`
* :ref:`Jinja2 template`
* :ref:`Select columns in Table with Regex`

UI:
^^^
* Improved look and feel of wizards
* Library wizard has new examples
* Node wizard can select tags
* Show filename in flow tab unless flow label has been explicitly set by user. This means that a flow created in 1.3.4 will have no flow label when opened in older versions.

Platform:
^^^^^^^^^
* More robust checks of port types
* Masked arrays

Deprecated nodes:
^^^^^^^^^^^^^^^^^
* Raw Tables nodes
* Scatter 3D ADAF



News in 1.3.3
-------------
Sympathy for Data version 1.3.3 offers improvements to existing nodes, the
table viewer and automatic parameter validation when configuring nodes.

GUI:
^^^^
* Behaviour change of “?” wildcard in :ref:`Table viewer<data_viewer>`
  :ref:`search bar <search_bar>` to match single character only
* General improvements of Table viewer GUI
* General improvements of parameter validation

New nodes/plugins:
^^^^^^^^^^^^^^^^^^
* New node: :ref:`Conditional error/warning`
* New node: :ref:`Cartesian product tuple2<Cartesian product tuple>`

Changes in nodes/plugins:
^^^^^^^^^^^^^^^^^^^^^^^^^
* Allow unicode characters in :ref:`Calculator<Calculator>` node
* Improved default behaviour of Calculator node
* Improved rescaling of preview plot in :ref:`Filter ADAFs` node
* Improved :ref:`XLSX export<Export Tables>` output compatibility
* :ref:`Extract Lambdas` can be configured when connected
* Improved performance of :ref:`VSplit Table`
* Improved bounds checking for calculator functions ``shift_seq_start`` and
  ``shift_seq_end``
* Improve gui in :ref:`Manually Create Table`. Now allows removing selected
  rows/columns as well as changing name and datatype of existing columns
* Improved handling of bad timebases in :ref:`interpolation nodes
  <Interpolate ADAF>`

APIs:
^^^^^
* Added ``value_changed`` propagation to parameters
* Made :ref:`verify_parameters <verify_parameters>` validate every change to
  configured parameters, for nodes with generated configurations

Miscellaneous:
^^^^^^^^^^^^^^
* Fixed update method for tuple type
* :reF:`data_viewer` can once again be run stand alone
* Updated icons



News in 1.3.2
-------------
Sympathy for Data version 1.3.2 offers several new and prominent features, such
as the ability to specify libraries used by workflows, new window handling
which brings open, but minimized, configurations and viewers into focus, a
reworked save dialog that properly detects changes in subflows and many
improvements to existing nodes.

GUI
^^^
* Raise open Configuration/Settings/Viewer windows on consecutive clicks
* Improved save confirmation for workflows
* Improvements to the function wizard. Including updating it to work with the
  new generic :ref:`F(x)` nodes

New features
^^^^^^^^^^^^
* Flows can now specify libraries and python paths in the Info dialog. These
  are added to the global library/python paths when loading the flow
* New error message box for node dialogs for showing validation errors/messages
  in node configurations
* Support for storing masked arrays, but not every node can handle them
  correctly

New nodes/plugins
^^^^^^^^^^^^^^^^^
* Figure nodes with support for Tables
* New version of :ref:`Transpose Table(s)<Transpose Table>`. These handle
  multiple rows and columns
* :ref:`Assert Equal Table`: for checking if two tables are equal. Mostly
  useful for testing purposes
* Generic :ref:`F(x)` nodes replacing all the previous type-specific f(x) nodes
* ATFX importer plugin for :ref:`ADAF`
* Set and Get nodes for :ref:`Table attributes<Get Table attributes>` and
  :ref:`Table column attributes<Get column attributes in Table>`
* :ref:`Propagate First Input (Same Type)`. Can be used for constraining
  type if needed.

Changes in nodes/plugins
^^^^^^^^^^^^^^^^^^^^^^^^
* Renamed Plot to Figure for nodes using the Figure type
* :ref:`Figure Compressor`, :ref:`Layout Figures in Subplots`: added auto
  recolor and auto rescale
* Improved datetime handling in Figure nodes
* MDF :ref:`exporter<Export ADAFs>` plugin: encode unicode columns instead of
  ignoring them
* :ref:`Convert columns in Table(s)<Convert columns in Table>`: converts string
  dates to either UTC or Naive datetimes. Choosing UTC, localized times will be
  converted to UTC. Choosing naive, the time zone info in the input is simply
  ignored. Old nodes will automatically use UTC
* Improved performance of :ref:`Select rows in Table(s)<Select rows in Table>`
* :ref:`Select rows nodes<Select rows in Table>` better handles values without
  explicit type annotation
* Improved error handling in :ref:`lookup nodes<Lookup Table>`
* :ref:`Calculator<Calculator>` plugin: Make sure that result is always
  correct length in changed_up, changed_down, and shift_array
* :ref:`Filter ADAFs`: added parameter validation and error messages. Filter
  design is computed and shown on parameter changes
* Changed the visible name for importer and exporter plugins for ADAF and Table
  to SyData
* Removes matlab settings from :ref:`Matlab Table`
  :ref:`nodes<Matlab Calculator>` and put them into global Preferences dialog
* Renamed calculator nodes to :ref:`Calculator(s)<Calculator>`
* CSV :ref:`Exporter<Export Tables>` plugin: improved writing of datetime
  columns
* Improve handling of missing units in :ref:`interpolate<Interpolate ADAF>`
  nodes

APIs
^^^^
* Extended :ref:`Table API<tableapi>` and added :class:`Column` object
* Change default value for attribute ``'unit'`` to always be empty string in
  ADAFs
* Added ParameterView base class for generated and custom GUIs to API. Custom
  GUIs can override the methods and properties to customize the behavior.
  Inheriting from ParameterView will be required in the future versions

Miscellaneous
^^^^^^^^^^^^^
* Added support for signing the Installer/Uninstaller
* Extended :ref:`searchbar<search_bar>` functionality for the :ref:`Table
  viewer<data_viewer>`
* Always write generated files in the right directory
* Fix overrides not saved in syx files
* Non-linked subflows inherit their parents $SY_FLOW_FILEPATH and $SY_FLOW_DIR
* Improve performance of type inference



News in 1.3.1
-------------
Sympathy for Data version 1.3.1 offers several new and prominent features such
as an improved data viewer with embedded plot, a new figure datatype and many new
nodes as well as improved performance and stability.

New features
^^^^^^^^^^^^
* Improved :ref:`data_viewer` with embedded plotting of signals.
* Overhaul of :ref:`subflow configuration<subflows>`: Split into settings and
  configuration. Removed grouping. Only allow selecting shallow
  nodes/flows. Added Wizard configuration mode. Optionally override parameters
  of linked subflows. Should be somewhat backwards compatible
* Added :ref:`Figure-type<figureapi>`. Passes serialized matplotlib figures between
  nodes
* Added tuple-type
* Better handling of broken links/nodes missing from library and changed port
  types due to subflow changes
* F(x) function wizard
* Allow setting flow name, description, version, author, and copyright
  information in flow info dialog. Also improved handling of flow labels all
  around
* Expose more :ref:`environment variables<default_workflow_vars>` from workflow
* New :ref:`command-line option<start_options>`: ``--nocapture`` for debugging

New nodes
^^^^^^^^^
* Figure-type nodes:
  :ref:`org.sysess.sympathy.visualize.figurefromtablewithtable`,
  :ref:`Figure Compressor`, :ref:`Layout Figures in Subplots`,
  :ref:`Export Figures`
* :ref:`Calculator<Calculator>` for a single Table added to Library
* New :ref:`Filter ADAFs` node with preview plots and improved configuration gui
* :ref:`Manually Create Table`
* Signal generator nodes for generating Table(s) of sinus, cosines or tangents
* :ref:`Matlab Tables` node
* :ref:`Hold value Table(s)<Hold value Table>`
* :ref:`Flatten list`
* ``Propagate Input`` and :ref:`Propagate First Input`. These can be used to
  implement some workarounds and for determining execution order in a flow
* :ref:`Interpolate ADAFs with Table`
* :ref:`Report Apply ADAFs with Datasources`
* :ref:`Filter rows in Tables`. This is the multiple Table version of existing
  Filter rows in Table
* Tuple nodes
* :ref:`Delete file`, which deletes a specified file from the file system

Node changes
^^^^^^^^^^^^
* Allow selection of multiple columns in :ref:`Unique Table`
* Allow choosing specific rasters in :ref:`Select category in ADAFs`
* Table attributes are merged for the :ref:`HJoin<HJoin Table>` nodes
* Allow setting fixed width/height for TextBoxes in :ref:`Report Template
  <Report Template Tables>`
* Easier date settings in :ref:`Plot Table`
* Rewrote :ref:`Matlab Tables` and :ref:`Matlab Calculator` nodes

Exporters/Importers changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ADAF Importer was extended with option to link to imported content
* MDF Importer can handle zip-files that include a single MDF-file as input
* Gzip Exporter binary writes files correctly
* ATF Importer supports a wider range of files
* Export tables nodes will now create output folders if necessary
* Increased compression for exported sydata-files produces smaller files

Optimizations
^^^^^^^^^^^^^
* Faster reading of writing of intermediate files
* Faster ADAF copy methods
* Improved length handling for tables
* Faster execution of :ref:`Select rows in Table(s)<Select rows in Table>`
* Faster execution of :ref:`Table` and :ref:`Select category in ADAFs`
* Responsive preview for :ref:`Calculator List` and :ref:`Calculator`

API changes
^^^^^^^^^^^
* Added MATLAB API for writing scripts executed by the Matlab node
* Added update method to Attributes class. (ADAF API)
* Added support for placeholder text in
  :ref:`lineedit_editor<parameter_editors>` in parameter helper
* Added visibility and enable/disable slots to ParameterValueWidget

Bug fixes
^^^^^^^^^
* Fixed name and type of output port of :ref:`Report Apply<Report Apply
  Tables>` nodes
* Fixed a bug where save file dialog wouldn’t show up at all when trying to
  save subflow on Windows, if the subflow label contained some specific
  unallowed characters
* Made sure that aborting a subflow doesn't also abort nodes outside of the
  subflow
* Fixed a bug where linked subflows were sometimes inserted with absolute path

Stability
^^^^^^^^^
* Improved reliability when working with lambdas, maps and apply nodes

Deprecated nodes
^^^^^^^^^^^^^^^^
Deprecated nodes don't show up in the library view, but can still be used in
workflows.

* Type specific versions of list operation nodes (such as Get Item Table and
  Append ADAF).
* Old FilterADAFs node


News in 1.3 series
------------------
Sympathy for Data version 1.3.0 offers several new and prominent features such
as generic types, higher order functions and much improved support for linked
subflows.

Many small improvements were made to the standard node library. Nodes will
often cope better with empty input data and deliver informative, but less
detailed, feedback.

Nodes from 1.2.x should be compatible with 1.3.0 but there are new, more
succinct, ways of writing nodes for 1.3.x that are not backwards compatible
with 1.2.x. When writing new nodes, consider which older versions of the
platform that will be used.


New features
^^^^^^^^^^^^
* :ref:`Generic types`
* :ref:`Higher order functions<higher_order_functions>`: Lambda, Map and Apply
* Official, and much improved, support for :ref:`linked subflows`
* Official support for :ref:`locked_subflows`
* New library structure using tags

New nodes
^^^^^^^^^
* New generic versions of all list operations
* :ref:`Ensure columns in Tables with Table`
* :ref:`Conditional Propagate`
* :ref:`Extract Lambdas` builtin node for reading lambda functions from existing
  workflows

User interface
^^^^^^^^^^^^^^
* Right-click on an empty part of the flow to insert
  :ref:`higher order functions<higher_order_functions>`.
* New command in context menu for inserting a subflow as a
  :ref:`link<linked subflows>`.
* Improved file dialogs in node configurations, by using native dialog when
  asking for an existing directory and starting file dialogs from currently
  selected file path.

API changes
^^^^^^^^^^^
* Simpler APIs for writing nodes. See :ref:`nodewriting`
* New method in :ref:`adafapi`: ``Group.number_of_rows``
* Configuration widgets can expose a method called save_parameters which is
  called before the gui is closed. See :ref:`custom_gui`
* Added API (parameter helper): List parameter widgets emit ``valueChanged``
  signal
* Improved slicing of (sy)table with slice object with negative or undefined
  stride
* Automatically update order, label, and description for parameters when the
  node’s definition changes
* :ref:`NodeContext <node_context>` is no longer a named tuple
* Added new method: :meth:`NodeContext.manage_input`. A managed input will have
  its lifetime decided outside of the node

Linked/locked subflows
^^^^^^^^^^^^^^^^^^^^^^
* Include subflows relative to path of parent flow, not relative to root
  flow. This affects where sympathy searches for linked subflows inside linked
  subflows and should hopefully feel more natural than the old system
* Allow opening of flows with broken links
* Import and export nodes can now be used inside locked subflows and lambdas
* Made it impossible for flows below a locked flow to themselves be locked
* Improved abort for locked subflows

Node changes
^^^^^^^^^^^^
* :ref:`Report<lib_reporting>` framework: histogram2d graph layer is now called
  heatmap and can handle different reduction functions (count, mean, median,
  max, min).
* Improved XLS(X) :ref:`import<Table>`/:ref:`export<Export Tables>`. Especially
  handling of dates, times, and mixed types. Cells formatted as Time are now
  imported as timedeltas.
* Renamed Sort Table(s) to :ref:`Sort rows in Table(s)<Sort rows in Table>`
* :ref:`Calculator List`: chooses columns case-sensitively on Windows too.
* :ref:`Calculator List`: shows number of output rows in preview in calculator gui.
* :ref:`VSplit Table`: Removed constraint that the index should be sorted. The
  elements will be grouped by the first occurrence of each unique value.
* :ref:`Convert columns in Table`: Added conversion path between datetime and
  float.
* :ref:`Select columns in ADAF with structure Table` now works as expected when
  *Remove selected* has been checked.
* :ref:`Select rows in Table with Table` offers a choice of reduction function
  between rows in config table. Previously it only read first row of the config
  table.
* "Slice List of ADAFs/Tables": Basic integer indexing now works as expected.
* Improve handling of one sample signals in :ref:`Interpolate ADAF(s)
  <Interpolate ADAF>`
* :ref:`Report Apply nodes <Report Apply Tables>` output datasources to created
  files
* Improved :ref:`CSV import<Table>`. Can now handle empty input, input with
  only one row, with or without trailing newline, and files with errors towards
  the end. It also features a new option for how to handle errors when
  importing a file. Header row has been made independent of the other input
  boxes, and no longer affects the data row. When read to end of file is
  selected, the number of footer rows is ignored. Delimiter detection was
  improved
* Fixed issues with nesting of higher order functions (:ref:`Map
  <Map>`, :ref:`Lambda<lambda_function>` and
  :ref:`Apply`)
* Improvements to :ref:`reporting <lib_reporting>`: Improved bin placement and
  x-axis extent of 1d histograms. Automatically set axes labels from data
  source if they are empty.  Added option "Lift pen when x decreases" to line
  graph layer. Added vline layer in reporting tool.
* Several nodes are better at forwarding attributes, table names, etc. to
  output :ref:`Slice data Table`, :ref:`Select columns in ADAF(s) with structure
  Table(s)<Select columns in ADAF with structure Table>`,
  :ref:`Unique Table(s)<Unique Table>`,
  :ref:`ADAF(s) to Table(s)<ADAF to Table>`, :ref:`Select rows in
  Table(s) with Table<Select rows in Table with Table>`,
  :ref:`Interpolate ADAF(s) <Interpolate ADAF>`, and :ref:`Rename columns nodes
  <Rename columns in Table>`
* Many nodes are better at handling missing or incomplete input data:
  :ref:`Filter Rows in Table`, :ref:`Replace values in Tables`,
  :ref:`Detrend ADAF(s) <Detrend ADAF>`, :ref:`ADAF(s) to Table(s)
  <ADAF to Table>`, :ref:`Select Report Pages`, :ref:`Scatter nodes
  <Scatter 3D Table>`.
* Added 'calculation' attribute on all output columns from :ref:`Calculator List`
  node
* :ref:`Export Tables` and :ref:`Archive files` create missing folders
* Fixed :ref:`Export Texts`

Other improvements
^^^^^^^^^^^^^^^^^^
* Added :ref:`default workflow environment variables <default_workflow_vars>`
  ``SY_FLOW_FILEPATH``, ``SY_FLOW_DIR`` and ``SY_FLOW_AUTHOR``. All flows have
  these and they can't be set or deleted.
* Subflows can define :ref:`workflow variables <flow_vars>`. Each subflow
  specializes the variables of its parent flow, so that the parent flows vars
  are accessible in the subflow but not vice versa.

* Improve performance by skipping validation of any nodes that don’t implement
  :meth:`verify_parameters`
* Improve performance by changing compression settings for sydata files,
  compression is faster but compresses slightly less
* Pretty print workflow xml files, making diffs possible

New requirements:

* Requiring pandas version 0.15 for the CSV import, for versions before 0.15
  down to 0.13 it will still work but may behave slightly differently in edge
  cases with blank rows


News in 1.2 series
------------------
Sympathy for Data version 1.2 is a significant minor release for Sympathy for
Data. It features several prominent new features, improved stability and more.
It is however not redesigned and with only a few small modifications, all
existing nodes and flows should work as well as in 1.1.

The bundled python installation has been upgraded with new versions of almost
every package. Added to the packages is scikit-learn, used for machine
learning. Our investigations suggest that the new package versions are
reasonably compatible with old nodes and cause no significant differences for
the standard library.


New features
^^^^^^^^^^^^
* Added support for using environment variables, and per installation/workflow
  variables. The variables which can have a default value are used in string
  fields of configuration widgets to enable parametrization. See
  :ref:`env_vars`.
* Added support for profiling, with the ability to produce graphs if Graphviz
  is available. See :ref:`profiling`.
* Added support for debugging single nodes with data available from Sympathy
  using spyder. See :ref:`spyder_debug`.
* Added new Node Wizard for generating new nodes. See :ref:`node_wizard`.
* Added support for configuring subflows by aggregating selected node
  configurations. See :ref:`subflow_config`.
* Improved support for plugins in third party libraries. It is no longer
  necessary to add the folder with the plugin to python path in preferences
* Support for adding custom data types in third party libraries. See
  :ref:`create_type`.
* Significantly improved handling of unicode paths including the ability to
  install Sympathy and third party libraries in a path with unicode characters

Nodes and plugins
^^^^^^^^^^^^^^^^^
* Added CarMaker type 2 ERG ADAF importer plugin called “CM-ERG”
* Plugins can now export to non-ascii filenames
* Fixed MDF export of boolean signals
* Added generating nodes for empty Table, Tables ADAF and ADAFs.
* Convert column nodes can convert to datetime
* Calculator node can produce compact output for length matched output
* Lookup nodes handles both event column and other columns with datetimes
* Time Sync nodes “SynchronizeLSF” strategy should work as expected again. The
  Vjoin index option is now only used for the ”Sync parts” strategy

New command line options
^^^^^^^^^^^^^^^^^^^^^^^^
See :ref:`start_options` for more info.

* Added new command line option, '--generate_documentation' for generating
  documentation from CLI
* Added 'exit_after_exception' argument which is activated by default in CLI.
  It makes Sympathy exit with error status if an unhandled exception occurs in
  a signal handler.
* Added separate flag: --node_loglevel, for controlling the log output from
  nodes.
* Made it possible to set the number of workers using --num_worker_processes n.

API changes
^^^^^^^^^^^
* Libraries must now have only a single python package in their Common folders.
  See :ref:`nodewriting`. In the Standard Library this package is called sylib
* Removed ``has_parameter_view`` from node interface. See :ref:`custom_gui`.
* Changed default unit for time series to empty string instead of ``'unknown'``.
* Added ``has_column`` method in sytable and added corresponding method in
  ``table.File``
* Accessing an ADAF basis which does not exist will raise a KeyError
* Improved node error handling, making it possible for nodes to issue user
  friendly error messages as well as warnings. See :ref:`node_errors`.
* Expanded and improved documentation, including API references for all default
  data types, and documentation on how to create your own data type
* Improved error handling in many data type API functions

User interface
^^^^^^^^^^^^^^
* Improved selection and context menu handling
* "Help" in node context menus will now also build documentation if necessary.
* Allow connections to be made by dragging from an input to an output port
* Added zoom with Ctrl/Cmd + scroll wheel
* Added working stop button.
* Improved the presentation of data in the viewer with a clearer font and
  better size handling as well as coloring of columns by data type
* Improved undo/redo functionality, making more operations available in the
  undo history

Stability
^^^^^^^^^
* Avoid hanging on Windows when too much output is produced during startup
* Avoid infinite wait during node validation
