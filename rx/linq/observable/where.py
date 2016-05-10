from functools import partial

from rx.internal.utils import adapt_call
from rx.core import SafeObserver


def where(predicate, source=None):
    """Filters the elements of an observable sequence based on a predicate
    by incorporating the element's index.

    1 - source.filter(lambda value: value < 10)
    2 - source.filter(lambda value, index: value < 10 or index < 10)

    Keyword arguments:
    :param Observable self: Observable sequence to filter.
    :param (T, <int>) -> bool predicate: A function to test each source element
        for a condition; the
        second parameter of the function represents the index of the source
        element.

    :returns: An observable sequence that contains elements from the input
    sequence that satisfy the condition.
    :rtype: Observable
    """
    if source is None:
        return partial(where, predicate)

    predicate = adapt_call(predicate)

    def subscribe(observer):
        safe_observer = None
        count = [0]

        def on_next(value):
            try:
                should_run = predicate(value, count[0])
            except Exception as ex:
                observer.on_error(ex)
                safe_observer.dispose()
            else:
                count[0] += 1

                if should_run:
                    observer.on_next(value)

        safe_observer = SafeObserver(on_next, observer.on_error, observer.on_completed)
        return source.subscribe_safe(safe_observer)
    return source.create(subscribe)
