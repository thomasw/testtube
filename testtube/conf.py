"""testtube settings module."""
import argparse
import os
import sys

# testube settings
SRC_DIR = None
PATTERNS = ()


def get_arguments():
    """Prompts the user for a source directory and an optional settings
    module.

    """
    parser = argparse.ArgumentParser(
        description='Watch a directory and run a custom set of tests whenever'
                    ' a file changes.')
    parser.add_argument(
        '--src_dir', type=str, default=os.getcwd(),
        help='The directory to watch for changes. (Defaults to CWD)')
    parser.add_argument(
        '--settings', type=str, default='tube',
        help='The testtube settings module that defines which tests to run.'
             ' (Defaults to "tube" - your settings module must be importable'
             ' from your current working directory)')
    args = parser.parse_args()

    return args.src_dir, args.settings


def _set_src_dir(src_dir):
    """Generate an absolute path by merging the cwd with the passed src dir"""
    global SRC_DIR

    SRC_DIR = os.path.realpath(os.path.join(os.getcwd(), src_dir))


def _get_test_suite_from_settings(settings_module):
    """Import settings_module and extract the relevant settings."""
    global PATTERNS

    sys.path.append(os.getcwd())
    settings = __import__(settings_module)

    PATTERNS = settings.PATTERNS


def configure(src_dir, settings):
    """Configure the app to use the specified SRC_DIR and extract the
    relevant settings from the specified settings module.

    """
    _set_src_dir(src_dir)
    _get_test_suite_from_settings(settings)
