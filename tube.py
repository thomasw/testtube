from testtube.helpers import Frosted, Nosetests, Pep257, Flake8

PATTERNS = (
    # Run pep257 check against a file if it changes, excluding files that have
    # test_ or tube.py in the name.
    # If this test fails, don't make any noise (0 bells on failure)
    (
        r'((?!test_)(?!tube\.py).)*\.py$',
        [Pep257(bells=0)]
    ),
    # Run flake8 and Frosted on all python files when they change. If these
    # checks fail, abort the entire test suite because it might be due to a
    # syntax error. There's no point running the subsequent tests if there
    # is such an error.
    (
        r'.*\.py$',
        [Flake8(all_files=True), Frosted(all_files=True)],
        {'fail_fast': True}
    ),
    # Run the test suite whenever python or test config files change
    (
        r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)',
        [Nosetests()]
    )
)
