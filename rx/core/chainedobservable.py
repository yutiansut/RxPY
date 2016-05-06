from . import AnonymousObservable

from rx.linq.observable.select import select
from rx.linq.observable.where import where
from rx.linq.observable.fromiterable import from_iterable


class ChainedObservable(AnonymousObservable):

    #
    # Creation
    #

    @classmethod
    def from_iterable(cls, iterable, scheduler=None):
        """Convert an array to an observable sequence, using an optional
        scheduler to enumerate the array.

        1 - res = rx.Observable.from_iterable([1,2,3])
        2 - res = rx.Observable.from_iterable([1,2,3], rx.Scheduler.timeout)

        Keyword arguments:
        :param Observable cls: Observable class
        :param Scheduler scheduler: [Optional] Scheduler to run the
            enumeration of the input sequence on.

        :returns: The observable sequence whose elements are pulled from the
            given enumerable sequence.
        :rtype: Observable
        """
        return cls(from_iterable(iterable, scheduler).subscribe)

    # Aliases
    from_ = from_iterable
    from_list = from_iterable

    #
    # Transformation
    #

    def select(self, selector):
        """Project each element of an observable sequence into a new form
        by incorporating the element's index.

        1 - source.map(lambda value: value * value)
        2 - source.map(lambda value, index: value * value + index)

        Keyword arguments:
        :param Callable[[Any, Any], Any] selector: A transform function to
            apply to each source element; the second parameter of the
            function represents the index of the source element.
        :rtype: Observable

        Returns an observable sequence whose elements are the result of
        invoking the transform function on each element of source.
        """
        return select(selector, self)

    def where(self, predicate):
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
        return where(predicate, self)
