from setuptools import setup, find_packages

from testtube import __version__, __author__
import sys

install_requires = ['watchdog==0.6.0']

tests_require = [
    'nose==1.2.1',
    'pep8==1.3.3',
    'pinocchio==0.3.1',
    'pyflakes==0.5.0',
]
# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
    tests_require.append('unittest2==0.5.1')

# Add Python 2.6 and 2.7-specific dependencies
if sys.version < '3':
    tests_require.append('mock==1.0.1')

setup(
    name='testtube',
    version=__version__,
    url='https://github.com/thomasw/testtube',
    download_url='https://github.com/thomasw/testtube/downloads',
    author=__author__,
    author_email='thomas.welfley+testtube@gmail.com',
    description='Testtube watches a specified directory for file changes '
                'and runs a set of defined tests against those files whenever '
                'a change occurs.',
    packages=find_packages(),
    scripts=['testtube/bin/stir'],
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='nose.collector',
)
