import unittest2 as unittest  # NOQA

try:
    from mock import call, Mock, patch, ANY  # NOQA
except ImportError:
    from unittest.mock import call, Mock, patch, ANY  # NOQA
