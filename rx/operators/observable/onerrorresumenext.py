from rx.core import Observable, ObservableBase, AnonymousObservable
from rx.disposables import CompositeDisposable, SingleAssignmentDisposable, \
    SerialDisposable
from rx.internal.utils import is_future


def on_error_resume_next(*args) -> ObservableBase:
    """Continues an observable sequence that is terminated normally or by
    an exception with the next observable sequence.

    1 - res = Observable.on_error_resume_next(xs, ys, zs)
    2 - res = Observable.on_error_resume_next([xs, ys, zs])

    Returns an observable sequence that concatenates the source sequences,
    even if a sequence terminates exceptionally.
    """
    # curently not in:
    # 3 - res = Observable.on_error_resume_next(xs, factory)

    if args and isinstance(args[0], list):
        sources = iter(args[0])
    else:
        sources = iter(args)

    def subscribe(observer, scheduler=None):
        subscription = SerialDisposable()
        cancelable = SerialDisposable()

        def action(scheduler, state=None):
            try:
                source = next(sources)
            except StopIteration:
                observer.on_completed()
                return

            # Allow source to be a factory method taking an error
            source = source(state) if callable(source) else source
            current = Observable.from_future(source) if is_future(source) else source

            d = SingleAssignmentDisposable()
            subscription.disposable = d

            def on_resume(state=None):
                scheduler.schedule(action, state)

            d.disposable = current.subscribe_(observer.on_next, on_resume, on_resume, scheduler)

        cancelable.disposable = scheduler.schedule(action)
        return CompositeDisposable(subscription, cancelable)
    return AnonymousObservable(subscribe)
