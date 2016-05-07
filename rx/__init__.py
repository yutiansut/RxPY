# flake8: noqa

try:
    import asyncio
except ImportError:
    try:
        import trollius as asyncio
    except ImportError:
        asyncio = None

try:
    from threading import RLock as Lock
except ImportError:
    from rx.internal.concurrency import NoLock as Lock

try:
    from asyncio import Future
except ImportError:
    try:
        from trollius import Future
    except ImportError:
        Future = None


# Rx configuration dictionary
config = {
    "Future": Future,
    "Lock": Lock,
    "asyncio": asyncio
}

from .core import Observer, Producer
from .core.anonymousobserver import AnonymousObserver
from .core.anonymousobservable import AnonymousObservable

from .linq.observable.select import select as map
from .linq.observable.where import where as filter
from .linq.observable.fromiterable import from_iterable
from_ = from_iterable

from rx.core import Observable

from . import backpressure
from . import linq


