from testtube.helpers import pep8_all, frosted_all, nosetests_all

PATTERNS = (
    (r'.*\.py$', [pep8_all, frosted_all, nosetests_all]),
)
