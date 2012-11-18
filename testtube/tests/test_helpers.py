import unittest2

from testtube import helpers


class Required(unittest2.TestCase):
    """helpers._required()"""
    def test_raises_an_exception_if_specified_module_is_not_available(self):
        self.assertRaises(ImportError, helpers._required, 'foo')

    def test_does_nothing_if_the_specified_module_is_available(self):
        self.assertIsNone(helpers._required('sys'))


class Shortpath(unittest2.TestCase):
    """helpers._short_path()"""
    def setUp(self):
        from testtube import conf
        conf.SRC_DIR = '/foo'

    def test_removes_SRC_DIR_from_the_passed_path(self):
        self.assertEqual(
            helpers._short_path("/foo/foo.py"), 'foo.py')
