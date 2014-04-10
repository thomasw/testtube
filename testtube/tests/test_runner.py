from . import Mock, unittest

from testtube.conf import Settings
from testtube import runner


class Inspect_pathTest(unittest.TestCase):
    """testtube.runner.inspect_path()"""
    def test_should_return_false_if_the_path_doesnt_match_the_pattern(self):
        match, kwargs = runner.inspect_path('no/matches/path/', r'kittens')
        self.assertFalse(match)

    def test_should_return_true_if_path_matches_the_pattern(self):
        match, kwargs = runner.inspect_path('kittens/', r'^kittens',)
        self.assertTrue(match)

    def test_should_return_named_subpatterns_if_any(self):
        match, kwargs = runner.inspect_path(
            'kittens/yay.py', r'(?P<dir>.*/).*.py')
        self.assertEqual(kwargs, {'dir': 'kittens/'})


class test_pathTest(unittest.TestCase):
    """testtube.runner.test_path()"""
    def setUp(self):
        self.callables = [Mock(), Mock(), Mock()]

    def test_should_pass_path_and_kwargs_to_a_set_of_callables(self):
        runner.test_path('yay/', self.callables, {'foo': 'bar'})

        for callable_mock in self.callables:
            callable_mock.asser_called_once_with(path='yay/', foo='bar')


class Run_testsTest(unittest.TestCase):
    """testtube.runner.run_tests()"""
    def setUp(self):
        self.mock_test = Mock()
        Settings.PATTERNS = ((r'.*', [self.mock_test]),)

    def test_should_call_tests_specified_in_conf_on_pattern_match(self):
        runner.run_tests('yay/')
        self.mock_test.assert_called_once_with('yay/')
