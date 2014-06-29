from setuptools import setup, find_packages

from testtube import __version__, __author__


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
    install_requires=['termcolor==1.1.0', 'watchdog==0.7.1'],
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
