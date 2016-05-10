from . import Observer
from rx.internal import noop, default_error
from rx.disposables import SingleAssignmentDisposable


class SafeObserver(Observer):

    def __init__(self, on_next, on_error=None, on_completed=None):
        super(SafeObserver, self).__init__()

        self.on_next = on_next or noop

        self._error = on_error or default_error
        self._completed = on_completed or noop

        self.sad = SingleAssignmentDisposable()

    def on_next(self, value):
        return NotImplemented

    def on_error(self, exn):
        try:
            self._error(exn)
        finally:
            self.dispose()

    def on_completed(self):
        try:
            self._completed()
        finally:
            self.dispose()

    @property
    def disposable(self):
        return self.sad

    @disposable.setter
    def disposable(self, value):
        self.sad.disposable = value

    def dispose(self):
        # This is much cheeper than using ObserverBase
        self.on_next = noop

        self._completed = noop
        self._error = default_error

        self.sad.dispose()

    def fail(self, exn):
        if self.sad.is_disposed:
            return False

        self._error(exn)
        return True
