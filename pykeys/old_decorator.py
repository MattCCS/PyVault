def requires_file_loaded(func):
    @functools.wraps(func)
    def _decorator(self, *args, **kwargs):
        if not self.table:
            raise errors.PasswordFileNotLoaded()
        func(self, *args, **kwargs)
    return _decorator
