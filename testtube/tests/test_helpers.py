from . import patch, unittest

from testtube.conf import Settings
from testtube import helpers


class SubprocessUsingHelperTest(unittest.TestCase):
    """TestCase with testtube.helpers.subprocess.call pre-patched."""
    def setUp(self):
        self.subprocess_patcher = patch("testtube.helpers.subprocess.call")
        self.subprocess_patcher = self.subprocess_patcher.start()


class Pep8HelperTest(SubprocessUsingHelperTest):
    def test_should_call_pep8_and_pass_it_the_specified_file(self):
        helpers.pep8('a.py')
        self.subprocess_patcher.assert_called_once_with(['pep8', 'a.py'])


class Pep8_allHelperTest(SubprocessUsingHelperTest):
    def test_should_call_pep8_against_the_entire_project(self):
        Settings.SRC_DIR = 'yay/'
        helpers.pep8_all('a.py')
        self.subprocess_patcher.assert_called_once_with(['pep8', 'yay/'])


class PyflakesHelperTest(SubprocessUsingHelperTest):
    def test_should_call_pyflakes_and_pass_it_the_specified_file(self):
        helpers.pyflakes('a.py')
        self.subprocess_patcher.assert_called_once_with(['pyflakes', 'a.py'])


class Pyflakes_allHelperTest(SubprocessUsingHelperTest):
    def test_should_call_pyflakes_and_pass_it_the_project_dir(self):
        Settings.SRC_DIR = 'yay/'
        helpers.pyflakes_all('')
        self.subprocess_patcher.assert_called_once_with(['pyflakes', 'yay/'])


class FrostedHelperTest(SubprocessUsingHelperTest):
    def test_should_call_frosted_and_pass_it_the_specified_file(self):
        helpers.frosted('a.py')
        self.subprocess_patcher.assert_called_once_with(['frosted', 'a.py'])


class Frosted_allHelperTest(SubprocessUsingHelperTest):
    def test_should_call_frosted_and_pass_it_the_project_dir(self):
        Settings.SRC_DIR = 'yay/'
        helpers.frosted_all('')
        self.subprocess_patcher.assert_called_once_with(
            ['frosted', '-r', 'yay/'])


class Nosetests_allHelperTest(SubprocessUsingHelperTest):
    def test_should_call_nosetests(self):
        helpers.nosetests_all('')
        self.subprocess_patcher.assert_called_once_with(['nosetests'])
