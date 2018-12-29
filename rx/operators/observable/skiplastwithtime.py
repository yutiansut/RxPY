from typing import Union
from datetime import timedelta

from rx.core import ObservableBase, AnonymousObservable
from rx.concurrency import timeout_scheduler


def skip_last_with_time(self, duration: Union[timedelta, int]) -> ObservableBase:
    """Skips elements for the specified duration from the end of the
    observable source sequence.

    1 - res = source.skip_last_with_time(5000)

    Description:
    This operator accumulates a queue with a length enough to store
    elements received during the initial duration window. As more
    elements are received, elements older than the specified duration
    are taken from the queue and produced on the result sequence. This
    causes elements to be delayed with duration.

    Keyword arguments:
    duration -- Duration for skipping elements from the end of the
        sequence.

    Returns an observable sequence with the elements skipped during the
    specified duration from the end of the source sequence.
    """

    source = self

    def subscribe(observer, scheduler=None):
        nonlocal duration

        scheduler = scheduler or timeout_scheduler
        duration = scheduler.to_timedelta(duration)
        q = []

        def on_next(x):
            now = scheduler.now
            q.append({"interval": now, "value": x})
            while len(q) and now - q[0]["interval"] >= duration:
                observer.on_next(q.pop(0)["value"])

        def on_completed():
            now = scheduler.now
            while len(q) and now - q[0]["interval"] >= duration:
                observer.on_next(q.pop(0)["value"])

            observer.on_completed()

        return source.subscribe_(on_next, observer.on_error, on_completed, scheduler)
    return AnonymousObservable(subscribe)
