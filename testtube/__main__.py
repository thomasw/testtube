"""Automatically runs a set of tests against a project on file update."""
import time

from watchdog.observers import Observer

import conf
from handlers import PyChangeHandler


if __name__ == '__main__':
    # Configure the app based on passed arguments
    conf.configure(*conf.get_arguments())

    observer = Observer()
    observer.schedule(PyChangeHandler(), conf.SRC_DIR, recursive=True)
    observer.start()

    print "testtube is now watching for changes...\n"

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
