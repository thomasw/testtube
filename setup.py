from setuptools import setup, find_packages

from testtube import __version__, __author__


setup(
    name="testtube",
    version=__version__,
    url='https://github.com/thomasw/testtube',
    download_url='https://github.com/thomasw/testtube/downloads',
    author=__author__,
    author_email='thomas.welfley+testtube@gmail.com',
    description='Testtube watches a specified directory for file changes '
                'and runs a set of defined tests against those files whenever'
                ' a change occurs.',
    packages=find_packages(),
    scripts=['testtube/bin/stir'],
    tests_require=["nose==1.2.1", "pinocchio==0.3.1", "unittest2==0.5.1",
                   "mock==1.0.1"],
    install_requires=['watchdog==0.6.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
    ],
    test_suite='nose.collector',
)
