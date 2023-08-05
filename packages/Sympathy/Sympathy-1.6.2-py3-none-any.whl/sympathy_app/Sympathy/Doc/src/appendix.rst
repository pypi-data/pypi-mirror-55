Appendix
========


.. _appendix_typed_text:

Input typed values as text
--------------------------

Some nodes will allow you to input text to use to produce a typed value - which
could depend, for example, on the type of columns used in the operation.  The
text needs to use a format that is understood by the functions for reading the
type used.

If the type is text, any input will do, but for other types see the following
examples:

    :bool: True, False, true, false, 1, 0
    :integer: 0, 1, 2, ...
    :float: 0, 0.0, 1, 1.1, ...
    :text: Anything goes here!
    :datetime: 1970-01-01T00:00:00.000000,
               1970-01-01 00:00:00.000000,
               1970-01-01 00:00:00.00,
               1970-01-01
    :timedelta: 1 days,
                2 d,
                44.333 seconds,
                2 days 2 h 44 seconds,
    :complex:  1.1 + 2j


.. _appendix_cli:

All command line options
------------------------


Top-level
^^^^^^^^^

``python -m sympathy_app --help``

.. code-block:: bash

   usage: __main__.py [-h] [--coverage COVERAGE]
                      {gui,cli,viewer,install,uninstall,tests,clear,launch,spyder,ipython,nosetests,pyflakes,pylint}
                      ...

   Sympathy for Data

   optional arguments:
     -h, --help            show this help message and exit
     --coverage COVERAGE   Enable computation of and store output in file
                           coverage.

   Commands:
     {gui,cli,viewer,install,uninstall,tests,clear,launch,spyder,ipython,nosetests,pyflakes,pylint}
                           Command
       gui                 run Sympathy in GUI mode
       cli                 run Sympathy in CLI mode
       viewer              run the viewer for sydata files.
       install             install Sympathy (start menu, file associations,
                           documentation)
       uninstall           uninstall Sympathy (start menu, file associations)
       tests               run the test suite
       clear               cleanup temporary files
       launch              internal use only
       spyder              external command help
       ipython             external command help
       nosetests           external command help
       pyflakes            external command help
       pylint              external command help


Gui and Cli
^^^^^^^^^^^

The options for the gui and cli commands are similar.

``python -m sympathy_app gui --help``

.. code-block:: bash

   usage: launch.py gui [-h] [--exit-after-exception {0,1}] [-v]
                        [-L {0,1,2,3,4,5}] [-N {0,1,2,3,4,5}]
                        [--num-worker-processes NUM_WORKER_PROCESSES]
                        [-C CONFIGFILE [CONFIGFILE ...]] [-I INIFILE]
                        [--nocapture]
                        [filename]

   positional arguments:
     filename              file containing workflow.

   optional arguments:
     -h, --help            show this help message and exit
     --exit-after-exception {0,1}, --exit_after_exception {0,1}
                           exit after uncaught exception occurs in a signal
                           handler
     -v, --version         show Sympathy for Data version
     -L {0,1,2,3,4,5}, --loglevel {0,1,2,3,4,5}
                           (0) disable logging, (5) enable all logging
     -N {0,1,2,3,4,5}, --node-loglevel {0,1,2,3,4,5}, --node_loglevel {0,1,2,3,4,5}
                           (0) disable logging, (5) enable all logging
     --num-worker-processes NUM_WORKER_PROCESSES, --num_worker_processes NUM_WORKER_PROCESSES
                           number of python worker processes (0) use system
                           number of CPUs
     -C CONFIGFILE [CONFIGFILE ...], --configfile CONFIGFILE [CONFIGFILE ...]
                           workflow configuration file, used to change parameters
                           and an optional outfile for the modified workflow
     -I INIFILE, --inifile INIFILE
                           settings ini-file to use instead of the default
     --nocapture           disable capturing of node output and send it directly
                           to stdout/stderr.


Viewer
^^^^^^

``python -m sympathy_app viewer --help``

.. code-block:: bash

   usage: __main__.py viewer [-h] [filename]

   positional arguments:
     filename    sydata file

   optional arguments:
     -h, --help  show this help message and exit

Install
^^^^^^^

``python -m sympathy_app install --help``

.. code-block:: bash

   usage: __main__.py install [-h] [--generate-all] [--generate-docs]
                              [--docs-library-dir DOCS_LIBRARY_DIR]
                              [--docs-output-dir DOCS_OUTPUT_DIR] [--compile]
                              [--compile-all] [--register] [--all]

   optional arguments:
     -h, --help            show this help message and exit
     --generate-all, --generate_all
                           generate parser files
     --compile             compile sympathy
     --compile-all, --compile_all
                           compile all site-package files
     --register            register application and create shortcuts
     --all                 perform full installation, includes all options if
                           enabled or by default if no other options are provided

     --generate-docs, --generate_docs
                           generate documentation files
     --docs-library-dir DOCS_LIBRARY_DIR, --docs_library_dir DOCS_LIBRARY_DIR
                           path to library to generate docs for, if not specified
                           generated documentation will be for the standard
                           library and platform
     --docs-output-dir DOCS_OUTPUT_DIR, --docs_output_dir DOCS_OUTPUT_DIR
                           choose folder in which to output generated docs


Uninstall
^^^^^^^^^

``python -m sympathy_app uninstall --help``

.. code-block:: bash

   usage: __main__.py uninstall [-h]

   optional arguments:
     -h, --help  show this help message and exit


Tests
^^^^^

``python -m sympathy_app tests --help``

.. code-block:: bash

   usage: __main__.py tests [-h] [-v]

   optional arguments:
     -h, --help     show this help message and exit
     -v, --verbose  verbose output

Clear
^^^^^


``python -m sympathy_app clear --help``

.. code-block:: bash

   usage: __main__.py clear [-h] [--caches] [--sessions]

   optional arguments:
     -h, --help  show this help message and exit
     --caches    Clear caches for Sympathy.
     --sessions  Clear sessions for Sympathy.
