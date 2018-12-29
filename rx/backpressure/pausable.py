
from rx.core import ObservableBase, Disposable
from rx.disposables import CompositeDisposable
from rx.subjects import Subject


class PausableObservable(ObservableBase):
    def __init__(self, source, pauser=None):
        self.controller = Subject()

        if pauser and hasattr(pauser, "subscribe"):
            self.pauser = self.controller.merge(pauser)
        else:
            self.pauser = self.controller

        super().__init__(source)

    def _subscribe_core(self, observer, scheduler=None):
        conn = self.source.publish()
        subscription = conn.subscribe(observer)
        connection = [Disposable.empty()]

        def on_next(value):
            if value:
                connection[0] = conn.connect()
            else:
                connection[0].dispose()
                connection[0] = Disposable.empty()

        pausable = self.pauser.distinct_until_changed().subscribe_(on_next, scheduler=scheduler)
        return CompositeDisposable(subscription, connection[0], pausable)

    def pause(self):
        self.controller.on_next(False)

    def resume(self):
        self.controller.on_next(True)

