"""Automatically runs a set of tests against a project on file update."""
import time

from watchdog.observers import Observer

from testtube.conf import get_arguments, Settings
from testtube.handlers import PyChangeHandler
from testtube.renderer import Renderer


def main():
    """Configure testtube and begins watching for file changes."""
    # Configure the app based on passed arguments
    Settings.configure(*get_arguments())
    renderer = Renderer()

    observer = Observer()
    observer.schedule(PyChangeHandler(), Settings.SRC_DIR, recursive=True)
    observer.start()

    renderer.notice(
        'testtube is now watching %s for changes...\n' % Settings.SRC_DIR)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
