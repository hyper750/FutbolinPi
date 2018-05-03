from abc import ABCMeta, abstractmethod

class MotionListener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def motion(self):
        pass