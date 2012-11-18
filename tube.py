from testtube.helpers import pep8, pyflakes, nosetests_all

PATTERNS = (
    (r'.*\.py', [pep8, pyflakes, nosetests_all]),
)
