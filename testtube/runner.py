"""Utilities for executing testtube suites against changed files."""
import re

from termcolor import colored

from testtube.conf import Settings
from testtube.helpers import HardTestFailure


class ResultCollection(list):

    """List representing results of testtube test group runs.

    Each entry in the list should be tuple containing a test (Helper subclass
    or other callable with a similar interface) and a result (bool).

    """

    @property
    def passed(self):
        """Return True if all the tests in the result collection passed."""
        return all(result for test, result in self)


class TestCollection(object):

    """Pattern, test list, and config grouping."""

    fail_fast_msg = colored('Fail fast is enabled. Aborting tests.', 'red')

    def __init__(self, pattern, tests, conf=None):
        """Build a test collection given a regex, a test list and configuration.

        Kwargs:
        pattern - a regular expression to match against paths of changed files
        tests - a list of callables to execute against a changed path
        conf - an optional configuration dict

        Valid conf keys:
        fail_fast - Causes the test run to abort if any tests in the group fail

        All other values in the conf dict are ignored by default.

        """
        self.pattern = pattern
        self.tests = tests
        self.conf = conf or {}

    @property
    def fail_fast(self):
        """Return True if the TestCollection is configured to fail fast.

        Fail fast collections abort subsequent test group processing if any
        tests in their group fail.

        """
        self.conf.get('fail_fast', False)

    def apply(self, path):
        """Run tests against a path if it matches the configured pattern.

        Returns a ResultCollection containg the success/fail status of the
        tests in the collection.

        """
        applicable, regex_match = self._check_path(path)
        results = ResultCollection()

        if not applicable:
            return results

        for test in self.tests:
            result = False

            try:
                result = test(path, regex_match)
            except HardTestFailure:
                result = False
                break
            finally:
                results.append((test, result))

        return results

    def _check_path(self, path):
        match = re.match(self.pattern, path)

        if not match:
            return False, {}

        return True, match


class SuiteRunner(object):
    fail_fast_msg = colored(
        'Aborting subsequent test groups. Fail fast enabled.', 'red')
    test_divider = '=' * 71

    def run(self, path):
        results = []

        for test_group in Settings.PATTERNS:
            tests = TestCollection(*test_group)
            result = tests.apply(path)

            if result:
                results.append(result)

            if result and not result.passed and tests.fail_fast:
                self._render_fail_fast_error()
                self._render_divider()
                break

            if result:
                self._render_divider()

        if results:
            self._render_test_report(results)

    def _render_divider(self):
        print self.test_divider

    def _render_fail_fast_error(self):
        print self.fail_fast_msg

    def _render_test_report(self, results):
        if not results:
            return

        print "Test Report\n"

        for count, suite_group in enumerate(results, 1):
            if not suite_group:
                continue

            test_group_results = "Test group %s:\t" % count

            for test, result in suite_group:
                color = 'green' if result else 'red'
                files = test.changed if not test.all_files else 'all matches'
                test_group_results += colored(
                    '%s (%s)\t' % (test.name, files), color)

            print test_group_results

        self._render_divider()
