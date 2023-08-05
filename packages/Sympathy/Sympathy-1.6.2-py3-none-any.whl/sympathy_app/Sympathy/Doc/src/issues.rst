.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2019 Combine Control Systems AB
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

.. _issues:

Reporting issues
================

In some cases Sympathy may fail to perform as expected.  Nodes that normally
work well may in some combination of configuration and input data behave in
undesired ways. For example, they could "crash" - producing a traceback - or
fail to produce reasonable results. Undesired behavior is not limited to nodes,
but also includes the platform itself. For example, failure to open particular
workflow files, application crashing, etc.

If you encounter undesired behavior along the lines outlined above, please feel
encouraged to report issues to allow us to learn from your experiences and try
to improve the application.

We try to make the issues anonymous and will not on purpose include personal or
sensitive information. Some basic information about the operating environment is
automatically included in the issue text. If there is anything automatically
included that you would like to leave out: simply edit the texts to change the
content of what is sent. Please check carefully, before sending, that the
information presented is something that you would like to share with us.


Issues with nodes
-----------------

Issues with nodes can be reported for any node from the standard library.
If you encountered issues after running, there might be some entry
in the *Messages* window. Right-clicking on such entries will allow you to
select *Report Issue* to open up the issue reporting form.

When creating issues this way, the text from the *Messages* window will be
be automatically included.


Issues with the platform
------------------------

In case of severe problems and problems with the platform, you can find the
*Report Issue* menu entry under the *Help* menu. This path allows you to author
issues freely, but does not help with including tracebacks like in the case of
issues reported for specific nodes. If you can find a reproducible way to make the
platform fail, try starting it with a console and check if a traceback or
severe warning text is found in the output, if so, include that in the details.
