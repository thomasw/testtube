Testtube
========

|Build Status| |Coverage Status| |Latest Version| |Downloads|

Spare your alt and tab keys by automatically running your project's test
suite whenever files change.

.. |Build Status| image:: https://img.shields.io/travis/thomasw/testtube.svg
   :target: https://travis-ci.org/thomasw/testtube
.. |Coverage Status| image:: https://img.shields.io/coveralls/thomasw/testtube.svg
   :target: https://coveralls.io/r/thomasw/testtube
.. |Latest Version| image:: https://img.shields.io/pypi/v/testtube.svg
   :target: https://pypi.python.org/pypi/testtube/
.. |Downloads| image:: https://img.shields.io/pypi/dm/testtube.svg
   :target: https://pypi.python.org/pypi/testtube/

Installation
------------

::

    pip install testtube

testtube is tested with Python 2.6, 2.7, 3.2, 3.3 and 3.4, 3.5 and pypy.

Usage
-----

1. Configure testtube
~~~~~~~~~~~~~~~~~~~~~

The simplest way to configure testtube is to place a tube.py file in
whatever directory testtube's watch command (``stir``) will be executed in
(this is typically a project's root directory). The tube.py file needs to define
an iterable named ``PATTERNS`` that contains tuples which 1. specify a regular
expression to test the paths of changed files and 2. an iterable containing a
list of tests to run when a path matches the corresponding regular expression.

Here's an example ``tube.py`` file:

.. code:: python

    from testtube.helpers import Frosted, Nosetests, Pep257, Flake8

    PATTERNS = (
        # Run pep257 check against a file if it changes, excluding files that have
        # test_ or tube.py in the name.
        # If this test fails, don't make any noise (0 bells on failure)
        (
            r'((?!test_)(?!tube\.py).)*\.py$',
            [Pep257(bells=0)]
        ),
        # Run flake8 and Frosted on the entire project when a python file changes.
        # If these checks fail, abort the entire test suite because failure might
        # be due to a syntax error. There's no point running the subsequent tests
        # if there is such an error.
        (
            r'.*\.py$',
            [Flake8(all_files=True), Frosted(all_files=True)],
            {'fail_fast': True}
        ),
        # Run the test suite whenever python or test config files change.
        (
            r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)',
            [Nosetests()]
        )
    )

In the example above, there are a series of patterns, coupled with a
list of callable tests generated via builtin helpers and, in one case,
an optional test group configuration.

A test, at its simplest, is just a method that returns ``True`` or
``False`` after being passed the path to a changed file and a regular
expression match object for the path's match against the test group's
regular expression. The example uses several helpers that ship with
testtube. These helpers are callable objects that can be configured in
various ways when they are instantiated.

Testtube comes with a number of these helpers, which can be found in
`helpers.py <https://github.com/thomasw/testtube/blob/master/testtube/helpers.py>`_.
They are designed to save consumers from specifying their own tests as much as
is possible. If they are insufficient for a specific project, please see
`Writing custom tests <#writing-custom-tests>`_.

Included helpers:

-  Pep8
-  Pyflakes
-  Frosted
-  Pep257
-  Nosetests
-  PythonSetupPyTest (runs python setup.py when matching files change)
-  ClearScreen

Helpers typically accept the following arguments when instantiated:

-  ``all_files``: run the test against the entire source directory
   instead of just the changed file (which is the default behavior)
-  ``fail_fast``: Abort running the rest of the test group if the test
   fails.
-  ``bells``: On failure, testtube will audibly notify the user 3 times
   unless otherwise specified
-  ``name``: The name of the test in test report output

The following generates a pep8 test configured to run against all files,
abort processing of its test group on failure, alert the user 5 times
audibly, and show up as "follow pep8 dude" in test report output:

.. code:: python

    from testtube.helpers import Pep8

    helper = Pep8(
        all_files=True, fail_fast=True, bells=5, name='follow pep8 dude')

Note that helpers, once instantiated, are just callables that return
``True`` or ``False``:

.. code:: python

    # Once configured, helpers are callables (they act like methods) that
    # accept a path to a python file and a regex match object (though the
    # match object isn't a requirement).

    helper('/path/to/some/file.py', None)

And here's that same example fully incorporated into a tube.py file:

.. code:: python

    from testtube.helpers import Pep8


    PATTERNS = [
        [
            # Pattern
            r'.*\.py$',
            # list of callable tests to run
            [
                Pep8(
                    all_files=True, fail_fast=True, bells=5,
                    name='follow pep8 dude')
            ]
        ]
    ]

The behavior of helpers can be customized as necessary by overriding
specific methods. See
`helpers.py <https://github.com/thomasw/testtube/blob/master/testtube/helpers.py>`_
for further information.

In addition to configuring helpers, test groups can also be configured:

-  ``fail_fast``: abort processing of subsequent test groups if all
   tests in the configured group did not pass.

In the first example tube.py file, the second test group is configured
to abort the rest of the test suite if either ``Flake8`` or ``Frosted``
fail.

2. Stir it
~~~~~~~~~~

Once a tube.py file is in place, tell testtube to watch the project for
changes:

::

    $ stir
    testtube is now watching /Path/to/CWD/ for changes...

By default, stir will watch the current working directory and configure
itself with a settings module named ``tube`` (tube.py). If the tube.py file was
placed in the project root directory, then one shouldn't need to specify
any parameters assuming stir is executed from that same directory. If paths need
to be customized a bit, ``stir -h`` will light the way:

::

    $ stir -h
    usage: stir [-h] [--src_dir SRC_DIR] [--settings SETTINGS]

    Watch a directory and run a custom set of tests whenever a file changes.

    optional arguments:
      -h, --help           show this help message and exit
      --src_dir SRC_DIR    The directory to watch for changes. (Defaults to CWD)
      --settings SETTINGS  Path to a testtube settings file that defines which
                           tests to run (Defaults to "tube.py" - your settings
                           file must be importable and the path must be relative
                           to your CWD)

Writing custom tests
--------------------

If the included helpers don't meet the specific needs of a project, custom tests
can be defined directly in tube.py. Simply define a callable that accepts two
arguments and add it to the ```PATTERNS`` list:

.. code:: python

    def mytest(changed_file, match_obj):
        print "Oh snap, %s just changed" % changed_file

    PATTERNS = (
        (r'.*', [mytest]),
    )

If a custom test needs to be configurable like the builtin helpers or if it
needs to make system calls, extending the base helper class
(``testtube.helpers.Helper``) and customizing the beahvior as is necessary is
usually the simplest approach. The following is a tube.py file which defines a
configureable test that outputs the file tree for the entire project each time a
python file changes:

.. code:: python

    from testtube.helpers import Helper


    class ProjectTree(Helper):
        # The built in helper class is designed to make writing tests that make
        # system calls easy. Overriding `command` is all that's usually
        # necessary
        command = 'tree'
        all_files = True

        def __init__(self, **kwargs):
            super(ProjectTree, self).__init__(kwargs)

            # TreeOutput only works on all files, so override any contrary
            # config
            self.all_files = True

    PATTERNS = (
        (r'.*\.py$', [ProjectTree(bells=1)]),
    )

Note that this example requires tree to be installed on the system
(``$ brew install tree`` for OS X users).

Caveats
-------

-  The distinction between ``r'.*\.py'`` and ``r'.*\.py$'`` is significant.
   Without the trailing ``$``, testtube will run tests everytime pyc
   files change. That's very likely to not be useful.
-  testtube doesn't currently reload its own configuration when it
   changes. If tube.py is modified, testtube will need to be restarted.

Local development
-----------------

Install the development requirements using the included requirements.txt file:

::

    pip install -r requirements.txt

It is often useful to use to use the checkout of testtube that's currently under
development to monitor itself using its included tube.py file. Use testtube to
help build testtube. This can be achieved by installing the checkout as an
editable. Execute the following from the project root and then use the `stir`
command as one usually would:

::

    pip install -e ./

Note that testtube will need to be restarted for code changes to take effect.

Everything else
---------------

Copyright (c) `Thomas Welfley <http://welfley.me>`_. See
`LICENSE <https://github.com/thomasw/testtube/blob/master/LICENSE>`_
for details.
