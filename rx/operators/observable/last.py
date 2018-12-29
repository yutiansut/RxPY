from typing import Callable
from rx.core import ObservableBase as Observable
from rx.core.typing import Predicate

from .lastordefault import last_or_default_async


def last(predicate: Predicate = None) -> Callable[[Observable], Observable]:
    """Returns the last element of an observable sequence that satisfies the
    condition in the predicate if specified, else the last element.

    Examples:
        >>> res = last()(source)
        >>> res = last(lambda x: x > 3)(source)

    Args:
        source - Observable sequence.
        predicate -- [Optional] A predicate function to evaluate for
            elements in the source sequence.

    Returns:
        A function that takes an observable source and returns a
        sequence containing the last element in the observable
        sequence that satisfies the condition in the predicate.
    """

    def partial(source: Observable) -> Observable:
        return source.filter(predicate).last() if predicate else last_or_default_async(source, False)
    return partial
