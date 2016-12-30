class FailTask(Exception):
    message = None
    exc = None

    def __init__(self, message=None, exc=None, **kwargs):
        from kombu.utils.encoding import safe_repr

        self.message = message

        if isinstance(exc, basestring):
            self.exc, self.excs = None, exc
        else:
            self.exc, self.excs = exc, safe_repr(exc) if exc else None

        Exception.__init__(self, message, exc, **kwargs)

    def __str__(self):
        if self.message:
            return self.message

        if self.excs:
            return self.excs

        return 'Failed task'
