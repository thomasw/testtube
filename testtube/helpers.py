"""Callables that accept a path to a file and check it for various things."""
import subprocess

from six import iteritems

from testtube.conf import Settings
from testtube.renderer import Renderer


class HardTestFailure(Exception):
    """Test failure that should abort test processing."""

    pass


class Helper(object):
    """Generic helper class for writing callable testtube tests.

    When a test that extends Helper is instantiated and called, it will:

    1. Set self.changed (path to changed file) and self.match
      (regex match object) to the passed in values.
    2. Call self.setup()
    3. Set result = self.test()
    4. If the test passed, it will call self.success(result)
    5. If the test failed, it will call self.failure(result)
    6. Call self.tear_down(result)
    7. Return the result

    self.test(), called in step 3, invokves the class attribute `command` via
    subporcess.call() and passes that command the arguments returned by
    get_args().

    Any method in the execution squence is overridable to enable helpers to be
    customized as necessary. See Helper subclasses for examples.

    """

    command = ''
    renderer = Renderer()

    def __init__(self, **kwargs):
        """Configure and return callable test.

        All keword arguments except `changed` and `match` are set as object
        attributes.

        """
        self.all_files = False
        self.fail_fast = False
        self.bells = 3
        self.name = self.__class__.__name__

        # Override default settings with passed in values.
        for setting, value in iteritems(kwargs):
            setattr(self, setting, value)

        # These properites are provided by __call__ and are not configurable.
        self.changed = ''
        self.match = ''

    def setup(self):
        """Prepare the helper class to execute the test."""
        changed = "source directory" if self.all_files else self.changed
        self.renderer.notice(
            'Executing %s against %s.\n' % (self.name, changed))

    def tear_down(self, result):
        """Clean up test execution."""
        self.renderer.notice()

    def success(self, result):
        """Handle test success."""
        self.renderer.success('Test passed.')

    def failure(self, result):
        """Hanlde test failure."""
        self.renderer.audible_alert(self.bells)
        self.renderer.failure('Test failed.')

        if self.fail_fast:
            raise HardTestFailure('Fail fast is enabled, aborting test run.')

    def test(self):
        """Execute the configured command with appropriate arguments."""
        if not self.command:
            return True

        return subprocess.call([self.command] + self.get_args()) == 0

    def get_args(self):
        """Generate argumnets for the test process."""
        if self.all_files:
            return [Settings.SRC_DIR]

        return [self.changed]

    def __call__(self, changed, match):
        """Test a changed file with the configured command."""
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
    """Execute PEP8 against a file or configured project directory."""

    command = 'pep8'


class Pyflakes(Helper):
    """Execute pyflakes against a file or configured project directory."""

    command = 'pyflakes'


class Frosted(Helper):
    """Execute pyflakes against a file or configured project directory."""

    command = 'frosted'

    def get_args(self):
        """Generate frosted arguments."""
        if self.all_files:
            return ['-r', Settings.SRC_DIR]

        return [self.changed]


class Nosetests(Helper):
    """Execute nosetests in the configured project directory.

    Note that this helper cannot be configured to run against only the
    changed file.

    """

    command = 'nosetests'

    def __init__(self, **kwargs):
        """Generate a `nosetests` callable.

        all_files=False will be ignored. This helper can only operate on
        all files.

        """
        kwargs['all_files'] = True
        super(Nosetests, self).__init__(**kwargs)

    def get_args(self, *args, **kwargs):
        """Return empty list of arguments.

        Nose can be configured via a setup.cfg file in settings.SRC_DIR

        """
        return []


class Flake8(Helper):
    """Execute flake8 against a file or configured project directory."""

    command = 'flake8'


class Pep257(Helper):
    """Execute pep257 against a file or configured project directory."""

    command = 'pep257'


class PythonSetupPyTest(Helper):
    """Execute `python setup.py test`."""

    command = 'python'

    def get_args(self):
        """Return list of arguments for `python`."""
        return ['setup.py', 'test']


class ClearScreen(Helper):
    """Clear the contents of the terminal window."""

    command = 'clear'

    def __init__(self, **kwargs):
        """Generate a `ClearScreen` callable.

        all_files=False will be ignored because this helper doesn't operate
        on specific files.

        """
        kwargs['all_files'] = True

        super(ClearScreen, self).__init__(**kwargs)

    def success(self, *args):
        """Output nothing on successs."""
        pass

    def setup(self):
        """Output nothing on test setup."""
        pass
