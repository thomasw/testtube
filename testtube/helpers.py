import subprocess
import sys

from testtube.conf import Settings


class HardTestFailure(Exception):
    pass


class Helper(object):
    command = ''
    all_files = False

    def setup(self, changed, *args, **kwargs):
        test_name = self.__class__.__name__

        if self.all_files:
            print "Executing %s against source directory.\n" % test_name
        else:
            print 'Executing %s against %s...\n' % (test_name, changed)

    def test(self, changed, *args, **kwargs):
        return self.execute_system_command(changed, *args, **kwargs)

    def tear_down(self, changed, result, *args, **kwargs):
        print 'Done.\n'

    def success(self, changed, result, *args, **kwargs):
        pass

    def failure(self, changed, result, *args, **kwargs):
        sys.stdout.write('\a' * 3)

        raise HardTestFailure("Fail fast is enabled, aborting test run.")

    def execute_system_command(self, changed, *args, **kwargs):
        if not self.command:
            return True

        return subprocess.call([self.command] + self.get_args(changed)) == 0

    def get_args(self, changed, *args, **kwargs):
        if self.all_files:
            return [Settings.SRC_DIR]

        return [changed]

    def __call__(self, changed, *args, **kwargs):
        self.setup(changed, *args, **kwargs)

        result = self.test(changed, *args, **kwargs)

        if result:
            self.success(changed, result, *args, **kwargs)

        if not result:
            self.failure(changed, result, *args, **kwargs)

        self.tear_down(changed, result, *args, **kwargs)


class Pep8(Helper):
    command = 'pep8'


class Pep8All(Pep8):
    all_files = True


class Pyflakes(Helper):
    command = 'pyflakes'


class PyflakesAll(Pyflakes):
    all_files = True


class Frosted(Helper):
    command = 'frosted'


class FrostedAll(Frosted):
    all_files = True

    def get_args(self, *args, **kwargs):
        return ['-r', Settings.SRC_DIR]


class NoseTestsAll(Helper):
    command = 'nosetests'
    all_files = True

    def get_args(self, *args, **kwargs):
        return []


pep8 = Pep8()
pep8_all = Pep8All()
pyflakes = Pyflakes()
pyflakes_all = PyflakesAll()
frosted = Frosted()
frosted_all = FrostedAll()
nosetests_all = NoseTestsAll()
