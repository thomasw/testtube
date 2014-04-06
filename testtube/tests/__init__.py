import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest  # NOQA
else:
    import unittest  # NOQA

if sys.version_info < (3,):
    from mock import Mock, patch  # NOQA
else:
    from unittest.mock import Mock, patch  # NOQA


# Frosted doesn't yet support noqa flags, so this hides the imported/unused
# complaints
Mock, patch, unittest
