.. _`node_reference`:

Node interface reference
========================
A node is defined as a Python class which inherits from
``sympathy.api.node.Node``. All node definitions should be in files with
filenames matching ``node_*.py`` and be placed in the Library folder of a node
library. Nodes can be placed in subfolders and multiple nodes can be defined in
the same file.


.. _`node_meta`:

Node definition
---------------
The following class variables make up the definition of a node.

.. note::

    The fields ``name`` and ``nodeid`` are needed to generate the node. If any
    of these two are missing any attempt at creating this node stops immediately
    without any error message. This can be a good way of e.g. creating a
    superclass for multiple node classes.

``name``
  *Required*.

  The name of the node, is what the user will rely on to identify the node. It
  will show in the library view and in the node's tooltip. It will also be used
  as the default label of any instance of the node in a flow.

  Try to keep the name short and to the point. For example adding "node" to
  the name of the node is rather pointless. It is also recommended to never
  have two nodes with the same name as they will be all but impossible for a
  user to tell apart.

``nodeid``
  *Required*.

  The nodeid is the identifier of the node. The node identifier must be unique
  for each node. It should look something like this:
  ``'com.example.boblib.helloworld'``. The node id should represent a kind of
  "path" to the node. It usually consists of the Internet domain name of your
  organization, the library name, perhaps some grouping in the library, and
  lastly the node name. It should not contain any spaces.

``author``
  The author of the node may contain name(s) of the author(s) of the node. It
  is only intended to give attribution to those who wrote the node. The current
  maintainer of the node can be specified in the library information in
  library.ini.

``version``
  A version number of the node, as a string. For example ``version = '1.0'``.

``icon``
  Path to a an icon to be displayed on the node, in SVG format (e.g.
  ``'path/to/icon.svg'``).

  Always use paths relative to the node in order for your library to be
  portable. Preferably use forward slashes as directory separators regardless
  of operating system.

  To create svg icons you can, for instance, use the free software Inkscape.

``description``
  The *description* variable is a short explanation of what the node does.
  This explanation is shown in tooltips in the GUI as well as in the
  documentation for the node. It is intended to help the user find out what the
  node does.

  It can be a paragraph of more than one line, but should still be short enough
  to be managable in a tootip in the GUI. It is recommended to write the
  description in imperative case (e.g. "Split Table row wise (vertically),
  grouping unique values of an index column.") with full punctuated sentences.
  When writing the description you can assume that the user has good knowledge
  of Sympathy in general, but knows nothing of what this specific node does. To
  keep it shorter it is recommended to only describe the most common mode(s) of
  operation for the node and not go into any details about edge cases, rarely
  used configuration options etc. Save those for the extended documentation (the
  docstring).

``related``
  A list of nodeids to nodes that are related to this one. Only used in
  documentation to guide the user to learn about nodes. If this has several
  variants (e.g. a table variant and a [table] variant) it should list all the
  others here. If a related node has several variants it is recommended to only
  list the most "basic" one in *related*.

``copyright``
  A copyright notice for this node. Note that this is generally not needed as a
  copyright notice can more easily be set for an entire library via
  :ref:`library_metadata`.

``inputs`` and ``outputs``
  The input and output ports of the node. Should be instances of
  ``sympathy.api.nodeconfig.Ports``. See :ref:`node_ports` for an introduction
  to how you add ports to nodes.

``parameters``
  Parameter definition. Can be either a dictionary or an OrderedDict. See
  :ref:`node_parameters` for an introduction.

``controllers``
  Controller definition. Gives a bit of extra control over the automatic
  configuration GUI. See :ref:`controllers`.


Node docstring
--------------
The docstring of a node class is used for documentation. This is a good place to
go into details about what the node does, its most important configuration and
(if applicable) how it handles errors; anything the user might need to know
about the node.

Note that the node's description is inserted at the top of the documentation so
the docstring doesn't need to repeat the description.

The docstring may include Sphinx `ReStructuredText
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
syntax. If you want to use ReST headings in your node documenation you should
use the equal sign (=) and hyphen (-) levels.


.. _overridable_node_methods:

Overridable node methods
------------------------
Override the following methods to specify the behavior of a node.

``adjust_parameters(self, node_context)``
  Adjust the parameters depending on the input data. See
  :ref:`adjust_parameters` for more details.

``execute(self, node_context)``
  *Required*

  Called when executing the node.

``exec_parameter_view(self, node_context)``
  Return a custom configuration widget. If this method is not implemented, a
  configuration widget is built automatically from the parameter definition.
  See :ref:`custom_gui` for more details.

``update_parameters(self, parameters)``
  Update the parameters of an old instance of the node to the new node
  definition, by making changes to the argument ``old_params``. Note that this
  method does not receive a node context object. It only receives the current
  parameters of the node. See :ref:`update_parameters` for more details.

.. _verify_parameters:

``verify_parameters(self, node_context)``
  Verify the parameters and return True if node is ready to be executed.
  As long as this method returns False the node will be in an invalid state and
  can not be executed. The configuration dialog can also not be accepted as long
  as this method returns False.


Callable node methods
---------------------
Utility methods available in the node methods.

.. _node_progress:

``self.set_progress(value)``
  Tell the user how many percent of the node's execution have been completed.
  The value should be between 0 and 100 inclusive. It is considered good
  practice to add calls to this method for any non-instant operations. For an
  example, see :ref:`Progress Example`.

  Calling this method in other node methods than ``execute`` has no
  effect.


.. _node_context:

Node context reference
----------------------
The node context object that is sent to most node methods has five fields:

``input`` and ``output``
  Input and output ports. See :ref:`node_ports` for an introduction to the use
  of ports.

  Each port will be an object of the data type of that port. A reference of
  each data type can be found here: :ref:`datatypeapis`.

  In ``execute`` the input ports will always have data, but in all
  other node methods it is possible that there is not yet any data on the input
  ports. See :ref:`adjust_parameters` for the basics of how to check if there
  is data available.

``parameters``
  The parameters of this instance of the node, as a parameter root object. See
  :ref:`node_parameters` for an introduction to the use of parameters, and
  :ref:`parameter_helper_reference` for a full reference of parameters in
  Sympathy.

``definition``
  Dictionary containing the full node definition.

``typealiases``
  Currently unused.


.. _list_node_decorator:

Node helper functions
---------------------
.. autofunction:: sympathy.api.node_helper.list_node_decorator
