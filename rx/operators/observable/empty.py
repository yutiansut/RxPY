from typing import Any

from rx.core import ObservableBase, Observer, AnonymousObservable, Disposable
from rx.concurrency import immediate_scheduler
from rx.core.abc.scheduler import Scheduler


def empty() -> ObservableBase:
    """Returns an empty observable sequence.

    1 - res = rx.Observable.empty()

    Returns an observable sequence with no elements.
    """

    def subscribe(observer: Observer, scheduler: Scheduler = None) -> Disposable:
        scheduler = scheduler or immediate_scheduler

        def action(_: Scheduler, __: Any) -> None:
            observer.on_completed()

        return scheduler.schedule(action)
    return AnonymousObservable(subscribe)
