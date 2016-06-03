from testtube.helpers import Nosetests, Pep257, Flake8, ClearScreen


PATTERNS = (
    # Clear the last set of test results because we're about to have more
    (
        r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)', [ClearScreen()],
    ),
    # Run pep257 check against a file if it changes, excluding files that have
    # tests/ or tube.py in the name.
    # If this test fails, don't make any noise (0 bells on failure)
    (
        r'((?!tests/)(?!tube\.py).)*\.py$',
        [Pep257(bells=0)]
    ),
    # Run flake8 on all python files when they change. If this checks fails,
    # abort the entire test suite because it might be due to a syntax error.
    # There's no point running the subsequent tests if there is such an error.
    (
        r'.*\.py$',
        [Flake8(all_files=True)],
        {'fail_fast': True}
    ),
    # Run the test suite whenever python or test config files change
    (
        r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)',
        [Nosetests()]
    )
)
