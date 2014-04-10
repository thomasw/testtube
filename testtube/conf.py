"""testtube settings module."""
import argparse
import imp
import os
import types


class Settings(types.ModuleType):
    # testube default settings
    CWD_SRC_DIR = ''
    SRC_DIR = os.getcwd()
    PATTERNS = ()

    @classmethod
    def configure(cls, src_dir, settings):
        """Configures testtube to use a src directory and settings module."""
        cls.CWD_SRC_DIR = src_dir
        cls.SRC_DIR = os.path.realpath(
            os.path.join(os.getcwd(), cls.CWD_SRC_DIR))
        cls.get_settings(settings)

    @classmethod
    def get_settings(cls, settings_module):
        """Set conf attributes equal to all uppercase attributes of settings"""
        settings = imp.load_source(
            'settings', os.path.join(os.getcwd(), settings_module))

        cls.PATTERNS = settings.PATTERNS

    @classmethod
    def short_path(cls, path):
        """Removes conf.SRC_DIR from a given path."""
        return path.partition("%s%s" % (cls.SRC_DIR, '/'))[2]


def get_arguments():
    """Prompts user for a source directory and an optional settings module."""
    parser = argparse.ArgumentParser(
        description='Watch a directory and run a custom set of tests whenever'
                    ' a file changes.')
    parser.add_argument(
        '--src_dir', type=str, default=os.getcwd(),
        help='The directory to watch for changes. (Defaults to CWD)')
    parser.add_argument(
        '--settings', type=str, default='tube.py',
        help='Path to a testtube settings file that defines which tests to run'
             ' (Defaults to "tube.py" - your settings file must be importable'
             ' and the path must be relative to your CWD)')
    args = parser.parse_args()

    return args.src_dir, args.settings
