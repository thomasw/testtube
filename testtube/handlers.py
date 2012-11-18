from watchdog.events import FileSystemEventHandler

from runner import run_tests


class PyChangeHandler(FileSystemEventHandler):
    """Watchdog handler that executes the test runner on file changes."""
    def on_any_event(self, event):
        run_tests(event.src_path)
