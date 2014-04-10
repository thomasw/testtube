import subprocess

from testtube.conf import Settings
from testtube.decorators import RequireModule


@RequireModule('pep8')
def pep8(changed, **kwargs):
    """Runs the pep8 checker against the changed file."""
    print 'Checking PEP 8 compliance of %s...\n' % Settings.short_path(changed)
    subprocess.call(['pep8', changed])
    print('\nDone.\n')


@RequireModule('pep8')
def pep8_all(changed, **kwargs):
    """Runs the pep8 checker against the entire project."""
    print 'Checking PEP 8 compliance of source directory...\n'
    subprocess.call(['pep8', Settings.SRC_DIR])
    print('\nDone.\n')


@RequireModule('pyflakes')
def pyflakes(changed, **kwargs):
    """Runs pyflakes against the changed file"""
    print 'Inspecting %s with pyflakes...\n' % Settings.short_path(changed)
    subprocess.call(['pyflakes', changed])
    print '\nDone.\n'


@RequireModule('pyflakes')
def pyflakes_all(changed, **kwargs):
    """Runs pyflakes against the entire project"""
    print 'Inspecting source directory with pyflakes...\n'
    subprocess.call(['pyflakes', Settings.SRC_DIR])
    print '\nDone.\n'


@RequireModule('frosted')
def frosted(changed, **kwargs):
    """Runs frosted against the changed file"""
    print 'Inspecting %s with frosted...\n' % Settings.short_path(changed)
    subprocess.call(['frosted', changed])
    print '\nDone.\n'


@RequireModule('frosted')
def frosted_all(changed, **kwargs):
    """Runs frosted against the entire project"""
    print 'Inspecting source directory with frosted...\n'
    subprocess.call(['frosted', '-r', Settings.SRC_DIR])
    print '\nDone.\n'


@RequireModule('nose')
def nosetests_all(changed, **kwargs):
    """Run nosetests against the entire project if any file changes."""
    print 'Running nosetests...'
    subprocess.call(['nosetests'])
