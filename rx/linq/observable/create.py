from rx.core import Observable, AnonymousObservable
from rx.internal import extensionclassmethod


@extensionclassmethod(Observable, alias="create_with_disposable")
def create(cls, subscribe):
    return cls(subscribe) if issubclass(cls, AnonymousObservable) else AnonymousObservable(subscribe)
