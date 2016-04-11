import os
import sys

from testtube.conf import Settings, get_arguments

from . import test_settings, unittest


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = test_settings
        self.settings = Settings
        self.settings.configure('foo/', 'tests/test_settings.py')


class SettingsModuleConfigureMethod(ConfTestCase):
    def test_should_set_the_SRC_DIR(self):
        """should set the SRC_DIR"""
        self.assertEqual(
            self.settings.SRC_DIR, os.path.join(os.getcwd(), 'foo'))

    def test_should_import_uppercased_settings_from_settings_module(self):
        self.assertEqual(self.settings.PATTERNS, self.settings.PATTERNS)


class SettingsModuleShortpathMethod(ConfTestCase):
    """Settings.short_path()"""
    def test_removes_SRC_DIR_from_the_passed_path(self):
        """removes Settings.SRC_DIR from the passed path"""
        sample_file = os.path.join(os.getcwd(), 'foo/sample.py')
        self.assertEqual(self.settings.short_path(sample_file), 'sample.py')


class GetArguments(unittest.TestCase):
    """get_arguments()"""
    def setUp(self):
        self.argv = sys.argv
        sys.argv = ['']
        self.args = get_arguments()
        self.default_path, self.default_settings_module = self.args

    def tearDown(self):
        sys.argv = self.argv

    def test_returns_thew_cwd_as_the_default_path(self):
        self.assertEqual(self.default_path, os.getcwd())

    def test_returns_tube_dot_py_as_the_default_settings_module_name(self):
        self.assertEqual(self.default_settings_module, 'tube.py')
