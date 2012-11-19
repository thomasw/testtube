# Testtube

Spare your alt and tab keys by automatically running your project's test suite
whenever files change.

Testtube uses [watchdog](https://github.com/gorakhargosh/watchdog/) to monitor
a given path for file changes. It could fairly be described as a simpler
(read: easier to use) implementation of watchdog's included "watchmedo"
utility.


## Installation


Before installing testtube, install argparse (one of testtube's dependencies
tends to blow up on install if argparse isn't already good to go):

    pip install argparse

Then, install testtube like you'd install any other python package:

    pip install testtube


## Usage


### Configure testtube

The simplest way to configure testtube is to drop a tube.py file in whatever
directory you'll be running `stir` from. The only thing that needs to be
in that file is a list of tuples named `PATTERNS` consisting of a regular
expression and a list of tests to run.

Here's an example:

    from testtube.helpers import pep8_all, pyflakes_all, nosetests_all

    PATTERNS = (
        (r'.*\.py', [pep8_all, pyflakes_all, nosetests_all]),
    )

Given the configuration above, testtube will match the full path to the
changed file against `r'.*\.py'`. If it matches, it will then run the
following tests: `pep8_all`, `pyflakes_all`, `nosetests_all`.

Testtube comes with a number of helpers, which you can find in
[helpers.py](https://github.com/thomasw/testtube/blob/master/testtube/helpers.py).
They are designed to save you from writing your own tests as much
as possible. If they don't meet your needs, see the "Writing your own tests"
section below.


### Stir it

    > stir
    testtube is now watching /Path/to/CWD/ for changes...

By default, stir will watch your current working directory and configure
itself with a settings module named `tube` (tube.py). If you dropped a tube.py
file into your project root, then you shouldn't need to specify any parameters
assuming you execute stir from that directory. If you've customized things a
bit, `stir -h` will light the way:

    usage: stir [-h] [--src_dir SRC_DIR] [--settings SETTINGS]

    Watch a directory and run a custom set of tests whenever a file changes.

    optional arguments:
      -h, --help           show this help message and exit
      --src_dir SRC_DIR    The directory to watch for changes. (Defaults to
                           CWD)
      --settings SETTINGS  The testtube settings module that defines which 
                           tests to run. (Defaults to "tube" - the settings
                           module must be importable from your current working
                           directory)


### Writing your own tests
If the included helpers don't do what you need, you can write your own tests
right in your settings module. Simply define a callable that accepts at least
one argument and add it to your patterns list:

    def mytest(changed_file):
        print "Oh snap, %s just changed" % changed_file
    
    PATTERNS = (
        (r'.*', [mytest]),
    )

Fortunately, tests can be a bit more clever than that. If you define it like
the following, testtube will pass it all of the named sub patterns in your
regular expression:

    def mysmartertest(changed_file, **kwargs):
        print "%s in %s/ changed." % (changed_file, kwargs['dir'])
    
    PATTERNS = (
        (r'.*/(?P<dir>[^/]*)/.*\.py', [mysmartertest]),
    )
    


## Everything else

Copyright (c) [Thomas Welfley](http://welfley.me). See
[LICENSE](https://github.com/thomasw/testtube/blob/master/LICENSE) for
details.
