from abc import ABCMeta, abstractmethod


class Producer(metaclass=ABCMeta):
    @abstractmethod
    def subscribe(self, observer):
        return NotImplemented
