from mock import Mock, patch
from . import unittest

from testtube.handlers import PyChangeHandler


class PyChangeHandlerTests(unittest.TestCase):
    """PyChangeHandler"""
    def setUp(self):
        self.handler = PyChangeHandler()

    @patch("testtube.handlers.run_tests")
    def test_should_execute_test_runner_with_changed_files(self, run_tests):
        self.handler.on_any_event(Mock(src_path='foo.py'))
        run_tests.assert_called_once_with('foo.py')
