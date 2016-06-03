"""Handlers that are invoked when file system changes occur."""
from watchdog.events import FileSystemEventHandler

from testtube.runner import SuiteRunner


class PyChangeHandler(FileSystemEventHandler):
    """Watchdog handler that executes the test runner on file changes."""

    def on_any_event(self, event):
        """Execute the test suite whenever files change."""
        test_runner = SuiteRunner()
        test_runner.run(event.src_path)
