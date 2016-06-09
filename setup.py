from codecs import open
import multiprocessing  # noqa `python setup.py test` fix for python 2.6
from setuptools import setup, find_packages
import sys

from testtube import __author__, __doc__, __version__


tests_require = ['nose==1.3.7', 'unittest2==1.1.0', 'spec==1.3.1']

if sys.version_info[:2] < (3, 3):  # mock was added to the stdlib in 3.3
    tests_require.append('mock==1.3.0')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('CHANGELOG.rst', 'r', 'utf-8') as f:
    changelog = f.read()

setup(
    name='testtube',
    version=__version__,
    url='https://github.com/thomasw/testtube',
    author=__author__,
    author_email='thomas.welfley+testtube@gmail.com',
    description=__doc__,
    long_description='%s\n\n%s' % (readme, changelog),
    packages=find_packages(),
    scripts=['testtube/bin/stir'],
    install_requires=['six>=1.2.0', 'termcolor==1.1.0', 'watchdog==0.8.3'],
    tests_require=tests_require,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'

    ],
    test_suite='nose.collector',
)
