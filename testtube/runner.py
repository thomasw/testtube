import re

from testtube.conf import Settings


def _inspect_path(path, pattern):
    """Return True if pattern matches path as well as the set of named
    subpattern matches.

    """
    match = re.match(pattern, path)

    if not match:
        return False, {}

    return True, match.groupdict()


def _test_path(path, tests, kwargs):
    """Runs a set of tests against a specified path passing kwargs to each."""
    for test in tests:
        test(path, **kwargs)


def run_tests(path):
    """Runs the corresponding tests if path matches in Settings.PATTERNS"""
    for pattern, tests in Settings.PATTERNS:
        run_tests, kwargs = _inspect_path(path, pattern)

        if run_tests:
            _test_path(path, tests, kwargs)
            print('=' * 58)
