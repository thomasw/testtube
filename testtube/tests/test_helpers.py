from mock import patch
import unittest2

from testtube import conf, helpers


class Required(unittest2.TestCase):
    """helpers._required()"""
    def test_raises_an_exception_if_specified_module_is_not_available(self):
        self.assertRaises(ImportError, helpers._required, 'foo')

    def test_does_nothing_if_the_specified_module_is_available(self):
        self.assertIsNone(helpers._required('sys'))


class Shortpath(unittest2.TestCase):
    """helpers._short_path()"""
    def setUp(self):
        conf.SRC_DIR = '/foo'

    def test_removes_SRC_DIR_from_the_passed_path(self):
        self.assertEqual(
            helpers._short_path("/foo/foo.py"), 'foo.py')


class SubprocessUsingHelperTest(unittest2.TestCase):
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
        conf.SRC_DIR = 'yay/'
        helpers.pep8_all('a.py')
        self.subprocess_patcher.assert_called_once_with(['pep8', 'yay/'])


class PyflakesHelperTest(SubprocessUsingHelperTest):
    def test_should_call_pyflakes_and_pass_it_the_specified_file(self):
        helpers.pyflakes('a.py')
        self.subprocess_patcher.assert_called_once_with(['pyflakes', 'a.py'])


class Pyflakes_allHelperTest(SubprocessUsingHelperTest):
    def test_should_call_pyflakes_and_pass_it_the_project_dir(self):
        conf.SRC_DIR = 'yay/'
        helpers.pyflakes_all('')
        self.subprocess_patcher.assert_called_once_with(['pyflakes', 'yay/'])


class Nosetests_allHelperTest(SubprocessUsingHelperTest):
    def test_should_call_nosetests(self):
        helpers.nosetests_all('')
        self.subprocess_patcher.assert_called_once_with(['nosetests'])
