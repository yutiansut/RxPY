from abc import ABCMeta, abstractmethod


class Producer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def subscribe(self, observer):
        return NotImplemented
