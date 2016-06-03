from . import ANY, Mock, patch, unittest

from testtube.helpers import HardTestFailure
from testtube.runner import ResultCollection, TestCollection, SuiteRunner


class ResultCollections(unittest.TestCase):
    """ResultCollections"""
    def setUp(self):
        self.passed_tests = ResultCollection([(Mock(), True), (Mock(), True)])
        self.mixed_result_tests = ResultCollection(
            [(Mock(), True), (Mock(), False)])

    def test_are_an_iterable(self):
        iter(self.passed_tests)

    def test_passed_property_is_true_if_all_tests_passed(self):
        self.assertTrue(self.passed_tests.passed)

    def test_passed_property_is_false_if_any_test_results_indicate_fail(self):
        self.assertFalse(self.mixed_result_tests.passed)


class TestCollectionTests(unittest.TestCase):
    def setUp(self):
        self.fake_passing_test = Mock()
        self.fake_passing_test.return_value = True
        self.fake_failing_test = Mock()
        self.fake_failing_test.return_value = False
        self.tests = [self.fake_passing_test, self.fake_failing_test]

        self.test_collection = TestCollection(
            r'.*', self.tests, {'fail_fast': True})


class TestCollections(TestCollectionTests):
    """TestCollections"""
    def test_instation_sets_conf_attribute(self):
        self.assertEqual(self.test_collection.conf, {'fail_fast': True})

    def test_instantiation_sets_pattern_attribute(self):
        self.assertEqual(self.test_collection.pattern, r'.*')

    def test_instantiation_sets_tests_attribute(self):
        self.assertEqual(self.test_collection.tests, self.tests)

    def test_fail_fast_attribute_returns_true_when_configured_to_true(self):
        """fail_fast attribute returns True when configured that way"""
        self.assertTrue(self.test_collection.fail_fast)


class TestCollectionApplyWhenPatternMatchesAgainstPath(TestCollectionTests):
    """TestCollection.apply() when pattern matches passed path"""
    def setUp(self):
        super(TestCollectionApplyWhenPatternMatchesAgainstPath, self).setUp()

        self.results = self.test_collection.apply('myfile.py')

    def test_runs_all_tests(self):
        for test in self.tests:
            test.assert_called_once_with('myfile.py', ANY)

    def test_returns_result_collection_with_entries_for_all_tests(self):
        self.assertEqual(
            self.results,
            [(self.fake_passing_test, True), (self.fake_failing_test, False)])


class TestCollectionApplyIfPatternDoesntMatchAgainstPath(TestCollectionTests):
    """TestCollection.apply() if pattern doesn't match against passed path"""
    def setUp(self):
        super(TestCollectionApplyIfPatternDoesntMatchAgainstPath, self).setUp()

        # Reconfigure the test collection to only run if the passed file is
        # foo.py
        self.test_collection.pattern = r'foo\.py'

        self.results = self.test_collection.apply('myfile.py')

    def test_returns_empty_result_collection(self):
        self.assertEqual(self.results, ResultCollection())

    def test_doesnt_execute_tests(self):
        for test in self.tests:
            self.assertFalse(test.called)


class TestCollectionApplyIfTestHasHardTestFailure(TestCollectionTests):
    """TestCollection.apply() if a test raises a HardTestFailure"""
    def setUp(self):
        super(TestCollectionApplyIfTestHasHardTestFailure, self).setUp()

        # Add a test that raises a HardTestFailure to the collection
        self.hard_test_failure = Mock()
        self.hard_test_failure.side_effect = HardTestFailure('failing')
        self.tests = [self.hard_test_failure] + self.tests

        self.test_collection.tests = self.tests

        self.results = self.test_collection.apply('myfile.py')

    def test_doesnt_execute_tests_after_the_raising_test(self):
        """doesn't execute tests after the raising test"""
        self.assertTrue(self.hard_test_failure.called)
        self.assertFalse(self.fake_passing_test.called)
        self.assertFalse(self.fake_failing_test.called)

    def test_returns_a_result_collection_with_raisig_test_as_failure(self):
        self.assertEqual(self.results, [(self.hard_test_failure, False)])


class SuiteRunnerTests(unittest.TestCase):
    """SuiteRunner.run()"""
    def setUp(self):
        self.test1, self.test2, self.test3 = Mock(), Mock(), Mock()
        self.test1.return_value = True
        self.test2.return_value = True
        self.test3.return_value = False

        SuiteRunner.renderer = Mock()

        settings_patcher = patch('testtube.runner.Settings')
        self.addCleanup(settings_patcher.stop)
        self.Settings = settings_patcher.start()
        self.Settings.PATTERNS = [
            (r'.*', [self.test1, self.test2]),
            (r'.*', [self.test3], {'fail_fast': True}),
            (r'.*', [])

        ]

        self.runner = SuiteRunner()
        self.runner.run('yay.py')

    def test_renders_a_result_report_with_list_of_result_groupings(self):
        self.runner.renderer.report.assert_called_once_with([
            [(self.test1, True), (self.test2, True)],
            [(self.test3, False)]
        ])

    def test_outputs_fail_fast_messaging_if_ff_test_group_fails(self):
        self.runner.renderer.failure.assert_called_once_with(
            'Aborting subsequent test groups. Fail fast enabled.')


class SuiteRunnerWithIgnorePatternsConfigured(unittest.TestCase):
    def setUp(self):
        SuiteRunner.renderer = Mock()
        self.test = Mock()

        settings_patcher = patch('testtube.runner.Settings')
        self.addCleanup(settings_patcher.stop)
        self.Settings = settings_patcher.start()

        self.Settings.PATTERNS = [(r'.*', [self.test])]
        self.Settings.IGNORE_PATTERNS = (r'yay\.txt',)

        self.runner = SuiteRunner()
        self.runner.run('yay.txt')

    def test_ignores_paths_matching_IGNORE_PATTERNS(self):
        self.test.assert_not_called()
