.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2010-2012 Combine Control Systems AB
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

.. _batch:

Using Sympathy from the command line
====================================

When Sympathy is installed in your python environment you can run
``python -m sympathy_app`` to access the command line interface.

For a comprehensive list of commands and options, see :ref:`appendix_cli`.

.. _launch_options:

Top-level commands
------------------

Running ``python -m sympathy_app --help`` will print the top level commands available.

``gui``
  run Sympathy in GUI mode
``cli``
  run Sympathy in CLI mode
``viewer``
  run the viewer for sydata files
``install``
  install Sympathy (start menu, file associations, documentation)
``uninstall``
  uninstall Sympathy (start menu, file associations, documentation)
``tests``
  run the test suite
``clear``
  cleanup temporary files

Furthermore there are a few external commands that can be started through
Sympathy in order to run them with the Sympathy environment setup correctly:

``spyder``, ``ipython``, ``nosetests``, ``pyflakes`` and ``pylint``.

.. _start_options:

Command options
---------------

As mentioned there are several top level commands. Most of which have
their own options.

In order to list the options available for a command, run sympathy_app adding
the desired command and ``--help`` to the command line. For example,
``python -m sympathy_app gui --help`` shows the available options for running
Sympathy in GUI mode.


Noteable examples
-----------------

Here are a few examples that might be useful, for the full list please use
the ``--help`` flag.


Run *Sympathy for Data GUI*:

.. code-block:: bash

   python -m sympathy_app gui

Run *Sympathy for Data CLI*, executing a specified syx-workflow-file:

.. code-block:: bash

   python -m sympathy_app cli filename


Build documentation for Sympathy for the platform and standard library.

.. code-block:: bash

   python -m symapthy_app install --generate-docs

Run the test suite

.. code-block:: bash

   python -m symapthy_app tests -v


Shortcuts
---------

Depending on how Sympathy was installed, you might also have shortcuts
available to some commands.

Wheel installer:

sympathy (``python -m sympathy_app``)
sympathy-cli (``python -m sympathy_app cli``)
sympathy-gui (``python -m sympathy_app gui``)

Windows installer:

RunSympathyCLI.bat (``python -m sympathy_app cli``)
RunSympathyGUI.bat (``python -m sympathy_app gui``)


.. _env_vars:

Using environment variables
---------------------------
Environment variable expansion is useful in node configurations where the node
should behave differently depending on the environment where it is executed.
A simple example would be a workflow that always loads a certain file from the
current user's home directory. To achieve that you can simply configure a
:ref:`Datasource` node to point to *$(HOME)/somefile.txt* and it will point to
the file *somefile.txt* in the user's home directory.

Apart from using already existing OS environment variables you can also add
your own environment variables at four different levels: OS/shell, local
config, workflow, and global config. Local config or workflow level variables
are generally preferred as they do not risk affecting workflows that they
should not affect.

.. _default_workflow_vars:

Default workflow environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A few variables are always defined in every workflow. ``$(SY_FLOW_FILEPATH)``
holds the full path to the workflow file, and ``$(SY_FLOW_DIR)`` contains the
directory of the workflow file. These variables behave just like normal workflow
variables, but they are not stored in a syx-file. Instead they are computed on the
fly when they are used. Check properties for a flow to see what values these
variables have for that flow.

.. _shell_vars:

Adding OS/shell environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setting environment variables or shell variables is done differently depending
on operating system, version, shell, and so on. As an example let us set the shell
variable ``GREETING`` and start Sympathy in a command prompt in Windows::

    > set GREETING=Hi!
    > RunSympathyGUI.exe

.. TODO : Write about OSX and linux?

Add a :ref:`Hello world Example` node and configure it to display
``$(GREETING)``. Run the node. The output should be *Hi!*.

Adding environment variables via local config files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When starting Sympathy with one or more :ref:`config files <config_files>`
specified you can set environment variables in those config files. Simply add
lines like this to the config file::

    $(GREETING) = "Yo!"

.. _flow_vars:

Adding workflow environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Workflow level environment variables can be added and removed via the
preferences GUI. Right click in your flow and click *Properties* and go to the
tab *Environment variables*, where you can add, change, and remove workflow
variables. These variables are stored in the workflow file, and will only
affect that workflow, and its subflows. A subflow can always override a
variable set by one of its parent flows.

Adding environment variables to the global config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just as workflow level variables, global config variables can be added and
edited under *File->Preferences...->Environment*, but they are stored in
the global config file for Sympathy so they affect all workflows.

Priority
^^^^^^^^
In case of name conflicts, environment variables are looked up in the following
order:

1. OS/shell
2. Local config files
3. Workflow (defined in current subflow)
4. Workflow (defined in a parent workflow)
5. Global config file


Special variables
^^^^^^^^^^^^^^^^^

**SY_OVERRIDE_TEMP_PATH**
    Used to override the folder where session data (temporary files) are
    stored. The temporary path may in turn contain environment variables.


.. _`config_files`:

Using config files
------------------

.. warning::

   This functionality is now deprecated, please do not use it unless there is no
   other alternative.

   Using the configuration port together with some normal input should be
   possible in most cases. See :ref:`configuration_port`.  Support for config
   files will be removed in Sympathy version 1.7.0 and later.


Examples
^^^^^^^^

Config files can be used to set environment variables and for directly changing
node config parameters.

Here is an example config file::

    alias helloworld = {1679abf7-2fb9-4453-9b45-a7eb61b670ed}
    helloworld.parameters.greeting.value = "Howdy!"

The crazy string of numbers and characters on the first line is a node UUID.
This uniquely identifies a single node in a workflow. The alias command is used
to give the node a more human-readable name that can be used throughout the
rest of the config file. To find the UUID of a node right click on it and
choose *Advanced->Properties*.

When setting strings with non-ASCII characters note that the config file should
always be encoded using utf8::

    alias helloworld = {1679abf7-2fb9-4453-9b45-a7eb61b670ed}
    helloworld.parameters.greeting.value = "Grüß Gott!"

Or use escape sequences for any non-ASCII characters::

    alias helloworld = {1679abf7-2fb9-4453-9b45-a7eb61b670ed}
    helloworld.parameters.greeting.value = "Gr\u00FC\u00DF Gott!"

When changing parameters in parameter groups or parameter pages write the full
path to the parameter. The following example changes the parameters of an
:ref:`All parameters example` node::

    alias allparameters = {9cc8b9b8-bcc5-4218-8bb4-13cf1e249626}
    allparameters.parameters.numbers.float.spinfloat.value = 0.005
    allparameters.parameters.logics.boolflag.value = false
    allparameters.parameters.strings.lineedit.value = "some string"

All values must be valid JSON, which for instance means that ``true`` and
``false`` are lower case.

When using multiple config files in the same call the last config file has
highest priority and the first one has the lowest priority::

    > RunSympathyGUI.exe flow.syx -C low_prio.cfg,high_prio.cfg

You can also add environment variables to your config files using the following
syntax::

    $(GREETING) = "Good day!"

Environment variables defined in config files have precedence over workflow
specific and global variables. For more info on environment variables see
:ref:`env_vars`.

Whenever you start Sympathy with a config file the flow that you open will be
copied to a temporary location and modified according to the config file. This
means that any relative paths in the flow or in the config file will be
relative to this temporary location instead of being relative to the original
workflow. So when using relative paths in conjunction with config files you
should always add an output workflow filename to the command::

    > RunSympathyGUI.exe flow.syx -C rel_paths.cfg output_flow.syx

Then the workflow *flow.syx* will be copied to *output_flow.syx* instead of a
default temporary location and you can use paths relative to the output
workflow path. Note that the output workflow will be mercilessly overwritten
each time you run the command above.
