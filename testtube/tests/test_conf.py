import os

from testtube.conf import Settings

from . import test_settings, unittest


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = test_settings
        self.settings = Settings
        self.settings.configure('foo/', 'testtube/tests/test_settings.py')


class SettingsModuleConfigureMethod(ConfTestCase):
    def test_should_set_the_SRC_DIR(self):
        """should set the SRC_DIR"""
        self.assertEqual(
            self.settings.SRC_DIR, os.path.join(os.getcwd(), 'foo'))

    def test_should_set_PATTERNS_to_setting_modules_PATTERNS_property(self):
        self.assertEqual(self.settings.PATTERNS, self.settings.PATTERNS)


class Shortpath(ConfTestCase):
    """Settings' short_path() method"""
    def test_removes_SRC_DIR_from_the_passed_path(self):
        """removes Settings.SRC_DIR from the passed path"""
        sample_file = os.path.join(os.getcwd(), 'foo/sample.py')
        self.assertEqual(self.settings.short_path(sample_file), 'sample.py')
