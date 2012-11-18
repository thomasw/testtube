import subprocess


def pep8(changed, **kwargs):
    """Runs the pep8 checker against the changed file."""
    _required('pep8')

    print 'Checking PEP 8 compliance of %s...\n' % _short_path(changed)
    subprocess.call(['pep8', changed])
    print '\nDone.\n'


def pyflakes(changed, **kwargs):
    """Runs pyflakes against the changed file"""
    _required('pyflakes')

    print 'Inspecting %s with pyflakes...\n' % _short_path(changed)
    subprocess.call(['pyflakes', changed])
    print '\nDone.\n'


def nosetests_all(changed, **kwargs):
    """Run nosetests against the entire project if any file changes."""
    _required('nose')

    print "Running nosetests..."
    subprocess.call(['nosetests'])


def _required(module_name):
    """If the specified module is not available, raise an import error with
    a helpful error.

    """
    try:
        __import__(module_name)
    except:
        raise ImportError(
            '%s must be installed to use this helper.' % module_name)


def _short_path(path):
    """Remove conf.SRC_DIRc from a given path."""
    import testtube.conf
    return path.partition("%s%s" % (testtube.conf.SRC_DIR, '/'))[2]
