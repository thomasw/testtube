# Testtube

[![Build Status](https://travis-ci.org/thomasw/testtube.png)](https://travis-ci.org/thomasw/testtube)
[![Coverage Status](https://coveralls.io/repos/thomasw/testtube/badge.png)](https://coveralls.io/r/thomasw/testtube)
[![Latest Version](https://pypip.in/v/testtube/badge.png)](https://pypi.python.org/pypi/testtube/)
[![Downloads](https://pypip.in/d/testtube/badge.png)](https://pypi.python.org/pypi/testtube/)

Spare your alt and tab keys by automatically running your project's test suite
whenever files change.

## Installation

Install testtube like you'd install any other python package:

```
pip install testtube
```

## Usage

### 1. Configure testtube

The simplest way to configure testtube is to drop a tube.py file in whatever
directory you'll be running the testtube watch command (`stir`) from.
The only thing that needs to be in that file is an iterable of tuples named
`PATTERNS` consisting of a regular expression and a list of tests to run.

Here's an example `tube.py` file from the testtube repo:

```python
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
```

In the example above, there are a series of patterns, coupled with a list of
callable tests generated via builtin helpers and, in one case, an optional test
group configuration.

A test, at its simplest, is just a method that returns `True` or `False` after
being passed the path to a changed file and a regular expression
match object for the path's match against the test group's regular expression.
The example uses several helpers that ship with testtube. These helpers
are callable objects that can be configured in various ways when they are
instantiated.

Testtube comes with a number of these helpers, which you can find in
[helpers.py](https://github.com/thomasw/testtube/blob/master/testtube/helpers.py).
They are designed to save you from writing your own tests as much
as possible. If they don't meet your needs, see
[Writing your own tests](#writing-your-own-tests).

Included helpers:

* Pep8
* Pyflakes
* Frosted
* Pep257
* Nosetests
* PythonSetupPyTest (runs python setup.py when matching files change)

Helpers typically accept the following arguments when instantiated:

* `all_files`: run the test against the entire source directory instead of just
  the changed file (which is the default behavior)
* `fail_fast`: Abort running the rest of the test group if the test fails.
* `bells`: On failure, testtube will audibly notify you 3 times unless otherwise
  specified
* `name`: The name of the test in test report output

The following generates a pep8 test configured to run against all files,
abort processing of its test group on failure, alert the user 5 times audibly,
and show up as "follow pep8 dude" in test report output:

```python
from testtube.helpers import Pep8

helper = Pep8(
    all_files=True, fail_fast=True, bells=5, name='follow pep8 dude')
```

Note that helpers, once instantiated, are just callables that return `True` or
`False`:

```python
# Once configured, helpers are callables (they act like methods) that
# accept a path to a python file and a regex match object (though the
# match object isn't a requirement).

helper('/path/to/some/file.py', None)
```

And here's that same example fully incorporated into a tube.py file:

```python
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
```

The behavior of helpers can be customized as necessary by overriding
specific methods. See [helpers.py](https://github.com/thomasw/testtube/blob/master/testtube/helpers.py)
for further information.

In additional to configuring helpers, test groups can also be configured:

* fail_fast: abort processing of subsequent test groups if all tests in the
  configured group did not pass.

In the first example tube.py file, the second test group is configured to abort
the rest of the test suite if either Flake8 or Frosted fail.

### 2. Stir it

Once you have a tube.py file, tell testtube to watch your project for changes:

    $ stir
    testtube is now watching /Path/to/CWD/ for changes...

By default, stir will watch your current working directory and configure
itself with a settings module named `tube` (tube.py). If you dropped a tube.py
file into your project root, then you shouldn't need to specify any parameters
assuming you execute stir from that directory. If you've customized things a
bit, `stir -h` will light the way:

```
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
```

### Writing your own tests

If the included helpers don't do what you need, you can write your own tests
right in your settings module. Simply define a callable that accepts two
arguments and add it to your patterns list:

```python
def mytest(changed_file, match_obj):
    print "Oh snap, %s just changed" % changed_file

PATTERNS = (
    (r'.*', [mytest]),
)
```

If you'd like to write tests that are configurable like the builtin helpers,
you can simply extend the base helper class. Here's a tube.py file that outputs
the file tree for the entire project each time a python file changes:

```python
from testtube.helpers import Helper


class ProjectTree(Helper):
    command = 'tree'
    all_files = True

    def __init__(self, **kwargs):
        super(ProjectTree, self).__init__()

        # TreeOutput only works on all files, so override any contrary config
        self.all_files = True

PATTERNS = (
    (r'.*\.py$', [ProjectTree(all_files=True)]),
)

```

Note that this example requires tree to be installed on your system
(`$ brew install tree` for OS X users).

## Everything else

Copyright (c) [Thomas Welfley](http://welfley.me). See
[LICENSE](https://github.com/thomasw/testtube/blob/master/LICENSE) for
details.
