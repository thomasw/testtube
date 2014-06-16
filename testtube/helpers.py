import subprocess
import sys

from termcolor import colored

from testtube.conf import Settings


class HardTestFailure(Exception):
    pass


class Helper(object):
    command = ''

    def __init__(self, **kwargs):
        self.all_files = False
        self.fail_fast = False
        self.bells = 3
        self.name = self.__class__.__name__

        # Override default settings with passed in values.
        for setting, value in kwargs.iteritems():
            setattr(self, setting, value)

        # These properites are provided by __call__ and are not configurable.
        self.changed = ''
        self.match = ''

    def setup(self):
        if self.all_files:
            print 'Executing %s against all matching files.\n' % self.name

        if not self.all_files:
            print 'Executing %s against %s...\n' % (self.name, self.changed)

    def tear_down(self, result):
        print

    def success(self, result):
        print colored('Test passed.', 'green')

    def failure(self, result):
        sys.stdout.write('\a' * self.bells)
        print colored('Test failed.', 'red')

        if self.fail_fast:
            raise HardTestFailure('Fail fast is enabled, aborting test run.')

    def test(self):
        if not self.command:
            return True

        return subprocess.call([self.command] + self.get_args()) == 0

    def get_args(self):
        if self.all_files:
            return [Settings.SRC_DIR]

        return [self.changed]

    def __call__(self, changed, match):
        self.changed = changed
        self.match = match

        self.setup()

        result = self.test()

        if result:
            self.success(result)

        if not result:
            self.failure(result)

        self.tear_down(result)

        return result


class Pep8(Helper):
    command = 'pep8'


class Pyflakes(Helper):
    command = 'pyflakes'


class Frosted(Helper):
    command = 'frosted'

    def get_args(self):
        if self.all_files:
            return ['-r', Settings.SRC_DIR]

        return [self.changed]


class Nosetests(Helper):
    command = 'nosetests'

    def __init__(self, **kwargs):
        super(Nosetests, self).__init__()

        # Nosetests only works on all files, so override any config for this
        # value.
        self.all_files = True

    def get_args(self, *args, **kwargs):
        return []


class Flake8(Helper):
    command = 'flake8'


class Pep257(Helper):
    command = 'pep257'
