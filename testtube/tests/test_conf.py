import imp
import os

from mock import patch
import unittest2

from testtube import conf


class ConfModule(unittest2.TestCase):
    def test_set_src_dir_should_set_the_src_dir(self):
        conf._set_src_dir('bar/')
        self.assertEqual(
            conf.SRC_DIR, os.path.join(os.getcwd(), 'bar'))

    @patch('__builtin__.__import__')
    def test_get_test_suite_from_settings_should_grab_settings(self, settings):
        # Create a fake settings module and make it the return value for
        # our __import__ mock
        fake_settings = imp.new_module('mysettings')
        fake_settings.PATTERNS = 'bar'
        settings.return_value = fake_settings

        conf._get_test_suite_from_settings('mysettings')

        self.assertEqual(conf.PATTERNS, 'bar')
        settings.assert_called_once_with('mysettings')
