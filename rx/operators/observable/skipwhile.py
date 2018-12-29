from typing import Any, Callable
from rx.core import ObservableBase, AnonymousObservable


def skip_while(source: ObservableBase, predicate: Callable[[Any], Any]) -> ObservableBase:
    """Bypasses elements in an observable sequence as long as a specified
    condition is true and then returns the remaining elements. The
    element's index is used in the logic of the predicate function.

    1 - source.skip_while(lambda value: value < 10)

    predicate -- A function to test each element for a condition; the
        second parameter of the function represents the index of the
        source element.

    Returns an observable sequence that contains the elements from the
    input sequence starting at the first element in the linear series that
    does not pass the test specified by predicate.
    """

    def subscribe(observer, scheduler=None):
        running = False

        def on_next(value):
            nonlocal running

            if not running:
                try:
                    running = not predicate(value)
                except Exception as exn:
                    observer.on_error(exn)
                    return

            if running:
                observer.on_next(value)

        return source.subscribe_(on_next, observer.on_error, observer.on_completed, scheduler)
    return AnonymousObservable(subscribe)


def skip_while_indexed(source: ObservableBase,
                       predicate: Callable[[Any, int], Any]
                      ) -> ObservableBase:
    """Bypasses elements in an observable sequence as long as a
    specified condition is true and then returns the remaining elements.
    The element's index is used in the logic of the predicate function.

    1 - source.skip_while(lambda value, index: value < 10 or index < 10)

    predicate -- A function to test each element for a condition; the
        second parameter of the function represents the index of the
        source element.

    Returns an observable sequence that contains the elements from the
    input sequence starting at the first element in the linear series
    that does not pass the test specified by predicate.
    """

    def subscribe(observer, scheduler=None):
        i, running = 0, False

        def on_next(value):
            nonlocal i, running

            if not running:
                try:
                    running = not predicate(value, i)
                except Exception as exn:
                    observer.on_error(exn)
                    return
                else:
                    i += 1

            if running:
                observer.on_next(value)

        return source.subscribe_(on_next, observer.on_error, observer.on_completed, scheduler)
    return AnonymousObservable(subscribe)
