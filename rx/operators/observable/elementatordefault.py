from typing import Any
from rx.core import ObservableBase, AnonymousObservable
from rx.internal.exceptions import ArgumentOutOfRangeException


def _element_at_or_default(source, index, has_default=False, default_value=None):
    if index < 0:
        raise ArgumentOutOfRangeException()

    def subscribe(observer, scheduler=None):
        i = [index]

        def on_next(x):
            found = False
            with source.lock:
                if i[0]:
                    i[0] -= 1
                else:
                    found = True

            if found:
                observer.on_next(x)
                observer.on_completed()

        def on_completed():
            if not has_default:
                observer.on_error(ArgumentOutOfRangeException())
            else:
                observer.on_next(default_value)
                observer.on_completed()

        return source.subscribe_(on_next, observer.on_error, on_completed, scheduler)
    return AnonymousObservable(subscribe)

def element_at_or_default(self, index: int, default_value: Any = None) -> ObservableBase:
    """Returns the element at a specified index in a sequence or a
    default value if the index is out of range.

    Example:
    res = source.element_at_or_default(5)
    res = source.element_at_or_default(5, 0)

    Keyword arguments:
    index -- The zero-based index of the element to retrieve.
    default_value -- [Optional] The default value if the index is
        outside the bounds of the source sequence.

    Returns an observable sequence that produces the element at the
        specified position in the source sequence, or a default value if
        the index is outside the bounds of the source sequence.
    """

    return _element_at_or_default(self, index, True, default_value)
