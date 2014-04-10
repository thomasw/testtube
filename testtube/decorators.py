from imp import find_module


class RequireModule(object):
    """Decorator that raises import error if specified module isn't found."""

    def __init__(self, module_name):
        self.module_name = module_name

    def _require_module(self):
        try:
            find_module(self.module_name)
        except ImportError:
            raise ImportError(
                '%s must be installed to use this helper.' % self.module_name)

    def __call__(self, func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            self._require_module()
            return func(*args, **kwargs)

        return wrapper
