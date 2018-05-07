from abc import ABCMeta, abstractmethod

class RestartListener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def restart(self):
        pass