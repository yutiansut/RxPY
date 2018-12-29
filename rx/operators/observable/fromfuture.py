from asyncio.futures import Future

from rx.core import ObservableBase, AnonymousObservable


def from_future(future: Future) -> ObservableBase:
    """Converts a Future to an Observable sequence

    Keyword Arguments:
    future -- A Python 3 compatible future.
        https://docs.python.org/3/library/asyncio-task.html#future
        http://www.tornadoweb.org/en/stable/concurrent.html#tornado.concurrent.Future

    Returns an Observable sequence which wraps the existing future
    success and failure.
    """

    def subscribe(observer, scheduler=None):
        def done(future):
            try:
                value = future.result()
            except Exception as ex:
                observer.on_error(ex)
            else:
                observer.on_next(value)
                observer.on_completed()

        future.add_done_callback(done)

        def dispose():
            if future and future.cancel:
                future.cancel()

        return dispose

    return AnonymousObservable(subscribe)
