import os
from multiprocessing import Process, Queue
import sys
from subprocess import call

from six.moves.queue import Empty
from unittest2 import TestCase

from testtube.core import main

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
STIR_PATH = os.path.join(PROJECT_ROOT, 'testtube/bin/stir')
SAMPLE_PROJECT = os.path.join(PROJECT_ROOT, 'sample')
SAMPLE_SETTINGS = os.path.join(SAMPLE_PROJECT, 'tube.py')


class TesttubeProc(Process):
    """Process wrapper for testtube."""

    def __init__(self, output):
        self.output = output

        super(TesttubeProc, self).__init__()

    def run(self):
        sys.argv = [
            STIR_PATH,
            '--src_dir=%s' % SAMPLE_PROJECT,
            '--settings=%s' % SAMPLE_SETTINGS
        ]
        sys.stdout = StdoutQueue(self.output)

        main()


class StdoutQueue(object):
    """sys.stdout stand in that directs writes to a multiprocessing.Queue."""

    def __init__(self, q):
        self.q = q

    def write(self, text):
        self.q.put(text)

        return len(text)


class OutputAccumulator(object):
    def __init__(self, queue):
        self.queue = queue
        self.output = ''

    def wait(self, text, increment=.1, timeout=5):
        total_time = 0

        while total_time < timeout:
            if text in self.output:
                return self.output

            try:
                self.output += self.queue.get(timeout=increment)
            except Empty:
                # To ensure that we aren't incrementing when we didn't have
                # to wait, we only increment in the event of an Empty exception
                # Technically, this implementation isn't accurate, but it's
                # close enough and solves the problem of needing to empty the
                # output queue with a separate loop before we start our get()
                # calls.
                total_time += increment

        return self.output

    def __str__(self):
        self.output


class IntegrationTest(TestCase):
    """TestCase that will execute stir in the context of the sample dir.

    To perform some action against sample/ that testtube should see, override
    the action method and perform that operation there.

    """
    def setUp(self):
        self.process = TesttubeProc(output=Queue())
        self.output_accumulator = OutputAccumulator(self.process.output)

        self.process.start()

        # wait for the process to startup and start monitoring for changes.
        # events triggered via self.touch will likely not be seen without this
        # line
        self.output_accumulator.wait('testtube is now')

        self.addCleanup(self.process.terminate)

    def touch(self, filename):
        """Touch a specified file in the sample directory.

        testtube will detect this as a change to the target file and will run
        any tests that match that file path.

        """
        call(['touch', os.path.join(SAMPLE_PROJECT, filename)])
