from typing import Any

from rx.core import ObservableBase, Observable


def of(*args: Any) -> ObservableBase:
    """This method creates a new Observable instance with a variable number
    of arguments, regardless of number or type of the arguments.

    Example:
    res = rx.Observable.of(1,2,3)

    Returns the observable sequence whose elements are pulled from the given
    arguments
    """
    return Observable.from_iterable(args)
