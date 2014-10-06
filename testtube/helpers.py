import subprocess

from testtube.conf import Settings
from testtube.renderer import Renderer


class HardTestFailure(Exception):
    pass


class Helper(object):
    command = ''
    renderer = Renderer()

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
        changed = "all matching files" if self.all_files else self.changed
        self.renderer.notice(
            'Executing %s against %s.\n' % (self.name, changed))

    def tear_down(self, result):
        self.renderer.notice()

    def success(self, result):
        self.renderer.success('Test passed.')

    def failure(self, result):
        self.renderer.audible_alert(self.bells)
        self.renderer.failure('Test failed.')

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


class PythonSetupPyTest(Helper):
    command = 'python'

    def get_args(self):
        return ['setup.py', 'test']
