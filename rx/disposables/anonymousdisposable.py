from threading import RLock

from rx.internal import noop
from rx.core.typing import Disposable, Dispose


class AnonymousDisposable(Disposable):
    """Main disposable class"""

    def __init__(self, action: Dispose = None) -> None:
        """Creates a disposable object that invokes the specified action
        when disposed.

        Keyword arguments:
        action -- Action to run during the first call to dispose. The
            action is guaranteed to be run at most once.

        Returns the disposable object that runs the given action upon
        disposal.
        """

        self.is_disposed = False
        self.action = action or noop

        self.lock = RLock()

        super().__init__()

    def dispose(self) -> None:
        """Performs the task of cleaning up resources."""

        dispose = False
        with self.lock:
            if not self.is_disposed:
                dispose = True
                self.is_disposed = True

        if dispose:
            self.action()
