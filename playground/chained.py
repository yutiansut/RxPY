import rx
from rx import ChainedObservable
from rx.core import AnonymousObservable
from rx.subjects import Subject


def main():
    print("-------------- Use normal chaining")

    # Chained like normal Rx
    xs = ChainedObservable.from_([1, 2, 3, 4, 5])
    ys = xs.where(lambda x: x > 2).select(lambda x: x*10)
    ys.subscribe(print)

    print("-------------- Functional style")

    # Functional style like itertools
    xs = rx.from_([1, 2, 3, 4, 5])
    ys = rx.map(lambda x: x*10, rx.filter(lambda x: x > 2, xs))
    ys.subscribe(print)

    print("-------------- Use subsclassing for extending")

    # Use subclassing to extend with own methods (open/closed)
    class MyObservable(ChainedObservable):
        def tap(self):
            """Extension method"""
            def subscribe(observer):
                def on_next(value):
                    print("Got value: %s" % value)
                    observer.on_next(value)
                return self.subscribe(on_next)
            return MyObservable(subscribe)

    xs = MyObservable.from_([1, 2, 3, 4, 5])
    ys = xs.where(lambda x: x > 2).select(lambda x: x*10).tap()
    ys.subscribe(print)

    print("-------------- Even subjects can be chained and extended")

    # Get subjects to understand extension methods
    s = Subject()
    xs = MyObservable(s)
    ys = xs.where(lambda x: x > 2).select(lambda x: x*10).tap()
    ys.subscribe(print)
    s.on_next(1)
    s.on_next(2)
    s.on_next(3)
    s.on_next(4)
    s.on_next(5)

    print("-------------- Extending with plain functions")

    # Functionally extended with plain functions
    def tap(source):
        def subscribe(observer):
            def on_next(value):
                print("Got value: %s" % value)
                observer.on_next(value)
            return source.subscribe(on_next)
        return AnonymousObservable(subscribe)

    xs = rx.from_([1, 2, 3, 4, 5])
    ys = tap(rx.map(lambda x: x*10, rx.filter(lambda x: x > 2, xs)))
    ys.subscribe(print)


if __name__ == '__main__':
    main()
