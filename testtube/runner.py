"""Utilities for executing testtube suites against changed files."""
import re

from testtube.conf import Settings
from testtube.helpers import HardTestFailure
from testtube.renderer import Renderer


def _check_path(pattern, path):
    """Using the specified pattern check the path to see if it matches."""
    match = re.match(pattern, path)

    if not match:
        return False, {}

    return True, match


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
        return self.conf.get('fail_fast', False)

    def apply(self, path):
        """Run tests against a path if it matches the configured pattern.

        Returns a ResultCollection containg the success/fail status of the
        tests in the collection.

        """
        applicable, regex_match = _check_path(self.pattern, path)
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


class SuiteRunner(object):
    """Execute matching test groups against a given path."""

    renderer = Renderer()

    def _ignore_path(self, path):
        for ignore_pattern in Settings.IGNORE_PATTERNS:
            ignore, match = _check_path(ignore_pattern, path)

            if ignore:
                return True

        return False

    def run(self, path):
        """Execute matching test groups against a given path."""
        results = []

        if self._ignore_path(path):
            return

        for test_group in Settings.PATTERNS:
            tests = TestCollection(*test_group)
            result = tests.apply(path)

            if not result:
                continue

            results.append(result)

            if not result.passed and tests.fail_fast:
                self.renderer.failure(
                    'Aborting subsequent test groups. Fail fast enabled.')
                self.renderer.divider()
                break

            self.renderer.divider()

        if results:
            self.renderer.report(results)
