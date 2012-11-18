from setuptools import setup, find_packages

from testtube import __version__, __author__


setup(
    name="testtube",
    version=__version__,
    url='https://github.com/thomasw/testtube',
    author=__author__,
    author_email='thomas.welfley+testtube@gmail.com',
    description='',
    packages=find_packages(),
    scripts=['testtube/bin/stir'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
    ],
)
