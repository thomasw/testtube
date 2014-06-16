import re

from termcolor import colored

from testtube.conf import Settings
from testtube.helpers import HardTestFailure


def inspect_path(path, pattern):
    """
    Return True and set of named subpattern matches if pattern matches path.
    """
    match = re.match(pattern, path)

    if not match:
        return False, {}

    return True, match


def test_path(path, test_group, groupdict):
    """Runs a set of tests against a specified path passing kwargs to each."""
    test_results = []

    for test in test_group:
        try:
            test_result = test(path, groupdict)
        except HardTestFailure:
            test_result = False
            print colored('\nFail fast is enabled. Aborting tests.\n', 'red')
            break
        finally:
            test_results.append((test, test_result))

    return test_results


def print_test_report(results):
    if not results:
        return

    print "Test Report\n"

    for count, suite_group in enumerate(results, 1):
        test_group_results = "Test group %s:\t" % count

        for test, result in suite_group:
            color = 'green' if result else 'red'
            files = test.changed if not test.all_files else 'all matches'
            test_group_results += colored(
                '%s (%s)\t' % (test.name, files), color)

        print test_group_results

    print('=' * 71)


def run_tests(path):
    """Runs the corresponding tests if path matches in Settings.PATTERNS"""
    suite_results = []

    for suite_conf in Settings.PATTERNS:
        # Ensure there are three elements in the tuple (the third element
        # in suite configs is optional)
        conf = suite_conf + ({}, ) if len(suite_conf) < 3 else suite_conf

        pattern, tests, group_conf = conf
        group_fail_fast = group_conf.get('fail_fast', False)

        run_tests, regex_match = inspect_path(path, pattern)

        if not run_tests:
            continue

        group_results = test_path(path, tests, regex_match)
        suite_results.append(group_results)
        all_passed = all(result for test, result in group_results)

        if not all_passed and group_fail_fast:
            print colored(
                'Aborting subsequent test groups. Fail fast enabled.', 'red')
            print('=' * 71)
            break

        print('=' * 71)

    print_test_report(suite_results)
