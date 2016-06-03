from testtube.helpers import Flake8


def simple_method_test(changed, match):
    return 'foo.bar' in changed

PATTERNS = (
    (
        r'.*\.py$', [Flake8(all_files=True)], {'fail_fast': True}
    ),
    (
        r'.*foo\.bar$', [simple_method_test]
    )
)
