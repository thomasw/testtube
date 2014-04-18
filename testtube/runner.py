import re

from testtube.conf import Settings
from testtube.helpers import HardTestFailure


def inspect_path(path, pattern):
    """
    Return True and set of named subpattern matches if pattern matches path.
    """
    match = re.match(pattern, path)

    if not match:
        return False, {}

    return True, match.groupdict()


def test_path(path, tests, kwargs):
    """Runs a set of tests against a specified path passing kwargs to each."""
    for test in tests:
        try:
            test(path, **kwargs)
        except HardTestFailure:
            print
            print "Test failed and fail fast is enabled. Aborting test run."
            print
            break


def run_tests(path):
    """Runs the corresponding tests if path matches in Settings.PATTERNS"""
    for pattern, tests in Settings.PATTERNS:
        run_tests, kwargs = inspect_path(path, pattern)

        if run_tests:
            test_path(path, tests, kwargs)
            print('=' * 58)
