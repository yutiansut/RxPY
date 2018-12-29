from rx.core import Observer, ObservableBase, AnonymousObservable, Disposable
from rx.disposables import CompositeDisposable


def do_action(source: ObservableBase, on_next=None, on_error=None, on_completed=None) -> ObservableBase:
    """Invokes an action for each element in the observable sequence and
    invokes an action on graceful or exceptional termination of the
    observable sequence. This method can be used for debugging, logging,
    etc. of query behavior by intercepting the message stream to run
    arbitrary actions for messages on the pipeline.

    1 - observable.do_action(send)
    2 - observable.do_action(on_next, on_error)
    3 - observable.do_action(on_next, on_error, on_completed)

    on_next -- [Optional] Action to invoke for each element in the
        observable sequence.
    on_error -- [Optional] Action to invoke on exceptional termination
        of the observable sequence.
    on_completed -- [Optional] Action to invoke on graceful termination
        of the observable sequence.

    Returns the source sequence with the side-effecting behavior
    applied.
    """

    def subscribe(observer, scheduler=None):
        def _on_next(x):
            if not on_next:
                observer.on_next(x)
            else:
                try:
                    on_next(x)
                except Exception as e:
                    observer.on_error(e)

                observer.on_next(x)

        def _on_error(exception):
            if not on_error:
                observer.on_error(exception)
            else:
                try:
                    on_error(exception)
                except Exception as e:
                    observer.on_error(e)

                observer.on_error(exception)

        def _on_completed():
            if not on_completed:
                observer.on_completed()
            else:
                try:
                    on_completed()
                except Exception as e:
                    observer.on_error(e)

                observer.on_completed()

        return source.subscribe_(_on_next, _on_error, _on_completed )
    return AnonymousObservable(subscribe)


def do(source: ObservableBase, observer: Observer) -> ObservableBase:
    """Invokes an action for each element in the observable sequence and
    invokes an action on graceful or exceptional termination of the
    observable sequence. This method can be used for debugging, logging,
    etc. of query behavior by intercepting the message stream to run
    arbitrary actions for messages on the pipeline.

    1 - observable.do(observer)

    observer -- Observer

    Returns the source sequence with the side-effecting behavior
    applied.
    """

    return source.do_action(observer.on_next, observer.on_error, observer.on_completed)


def do_after_next(source, after_next):
    """Invokes an action with each element after it has been emitted downstream.
    This can be helpful for debugging, logging, and other side effects.

    after_next -- Action to invoke on each element after it has been emitted
    """

    def subscribe(observer, scheduler=None):

        def on_next(value):
            try:
                observer.on_next(value)
                after_next(value)
            except Exception as e:
                observer.on_error(e)

        return source.subscribe_(on_next, observer.on_error, observer.on_completed)
    return AnonymousObservable(subscribe)


def do_on_subscribe(source: ObservableBase, on_subscribe):
    """Invokes an action on subscription.

    This can be helpful for debugging, logging, and other side effects
    on the start of an operation.

    Args:
        on_subscribe: Action to invoke on subscription
    """
    def subscribe(observer, scheduler=None):
        on_subscribe()
        return source.subscribe_(observer.on_next, observer.on_error, observer.on_completed, scheduler)

    return AnonymousObservable(subscribe)


def do_on_dispose(source: ObservableBase, on_dispose):
    """Invokes an action on disposal.

     This can be helpful for debugging, logging, and other side effects
     on the disposal of an operation.

    Args:
        on_dispose: Action to invoke on disposal
    """

    class OnDispose(Disposable):
        def dispose(self):
            on_dispose()

    def subscribe(observer, scheduler=None):
        composite_disposable = CompositeDisposable()
        composite_disposable.add(OnDispose())
        disposable = source.subscribe_(observer.on_next, observer.on_error, observer.on_completed, scheduler)
        composite_disposable.add(disposable)
        return composite_disposable

    return AnonymousObservable(subscribe)


def do_on_terminate(source, on_terminate):
    """Invokes an action on an on_complete() or on_error() event.
     This can be helpful for debugging, logging, and other side effects
     when completion or an error terminates an operation.


    on_terminate -- Action to invoke when on_complete or throw is called
    """

    def subscribe(observer, scheduler=None):

        def on_completed():
            try:
                on_terminate()
            except Exception as err:
                observer.on_error(err)
            else:
                observer.on_completed()

        def on_error(exception):
            try:
                on_terminate()
            except Exception as err:
                observer.on_error(err)
            else:
                observer.on_error(exception)

        return source.subscribe_(observer.on_next, on_error, on_completed, scheduler)
    return AnonymousObservable(subscribe)


def do_after_terminate(source, after_terminate):
    """Invokes an action after an on_complete() or on_error() event.
     This can be helpful for debugging, logging, and other side effects when completion or an error terminates an operation


    on_terminate -- Action to invoke after on_complete or throw is called
    """
    def subscribe(observer, scheduler=None):

        def on_completed():
            observer.on_completed()
            try:
                after_terminate()
            except Exception as err:
                observer.on_error(err)

        def on_error(exception):
            observer.on_error(exception)
            try:
                after_terminate()
            except Exception as err:
                observer.on_error(err)

        return source.subscribe(observer.on_next, on_error, on_completed, scheduler)
    return AnonymousObservable(subscribe)


def do_finally(source, finally_action):
    """Invokes an action after an on_complete(), on_error(), or disposal
    event occurs.

    This can be helpful for debugging, logging, and other side effects
    when completion, an error, or disposal terminates an operation.

    Note this operator will strive to execute the finally_action once,
    and prevent any redudant calls

    finally_action -- Action to invoke after on_complete, on_error, or disposal is called
    """

    class OnDispose(Disposable):
        def __init__(self, was_invoked):
            self.was_invoked = was_invoked

        def dispose(self):
            if not self.was_invoked[0]:
                finally_action()
                self.was_invoked[0] = True

    def subscribe(observer, scheduler=None):

        was_invoked = [False]

        def on_completed():
            observer.on_completed()
            try:
                if not was_invoked[0]:
                    finally_action()
                    was_invoked[0] = True
            except Exception as err:
                observer.on_error(err)

        def on_error(exception):
            observer.on_error(exception)
            try:
                if not was_invoked[0]:
                    finally_action()
                    was_invoked[0] = True
            except Exception as err:
                observer.on_error(err)

        composite_disposable = CompositeDisposable()
        composite_disposable.add(OnDispose(was_invoked))
        disposable = source.subscribe_(observer.on_next, on_error, on_completed, scheduler)
        composite_disposable.add(disposable)

        return composite_disposable

    return AnonymousObservable(subscribe)

