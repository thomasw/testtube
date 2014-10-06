from . import Mock, patch, unittest

from testtube.handlers import PyChangeHandler


class PyChangeHandlerTests(unittest.TestCase):
    """PyChangeHandler"""
    def setUp(self):
        self.handler = PyChangeHandler()

    @patch("testtube.handlers.SuiteRunner")
    def test_should_execute_test_runner_with_changed_files(self, test_runner):
        self.handler.on_any_event(Mock(src_path='foo.py'))
        test_runner.return_value.run.assert_called_once_with('foo.py')
