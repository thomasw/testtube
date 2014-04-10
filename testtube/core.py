"""Automatically runs a set of tests against a project on file update."""
import time

from watchdog.observers import Observer

from testtube.conf import get_arguments, Settings
from testtube.handlers import PyChangeHandler


def main():
    # Configure the app based on passed arguments
    Settings.configure(*get_arguments())

    observer = Observer()
    observer.schedule(PyChangeHandler(), Settings.SRC_DIR, recursive=True)
    observer.start()

    print('testtube is now watching %s for changes...\n' % Settings.SRC_DIR)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
