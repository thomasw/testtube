import os
import sys

from testtube import conf

from . import test_settings, unittest


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        # Add the tests dir to sys.path so test_settings is importable by
        # testtube's conf module
        sys.path.append(os.path.dirname(__file__))

        self.settings = test_settings
        self.conf = conf
        self.conf.configure('foo/', 'test_settings')


class ConfModuleConfigureMethod(ConfTestCase):
    def test_should_set_the_SRC_DIR(self):
        """should set the SRC_DIR"""
        self.assertEqual(self.conf.SRC_DIR, os.path.join(os.getcwd(), 'foo'))

    def test_should_set_PATTERNS_to_setting_modules_PATTERNS_property(self):
        self.assertEqual(self.conf.PATTERNS, self.settings.PATTERNS)


class Shortpath(ConfTestCase):
    """conf.short_path()"""
    def test_removes_SRC_DIR_from_the_passed_path(self):
        """removes SRC_DIR from the passed path"""
        sample_file = os.path.join(os.getcwd(), 'foo/sample.py')
        self.assertEqual(conf.short_path(sample_file), 'sample.py')
