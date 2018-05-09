import threading
import time
from abc import ABCMeta, abstractmethod

class StartListener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        pass

class RestartListener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def restart(self):
        pass

class Pooling(threading.Thread):
    def __init__(self, poolingTime):
        threading.Thread.__init__(self)
        self.__lock = threading.Lock()
        self.__seguirThread = False
        self.__restartListener = None
        self.__startListener = None
        #Time seconds to ms
        self.__poolingTime = poolingTime * 100

    def setStartListener(self, listener):
        if isinstance(listener, StartListener):
            self.__startListener = listener

    def setRestartListener(self, listener):
        if isinstance(listener, RestartListener):
            self.__restartListener = listener

    def threadIsRunning(self):
        with self.__lock:
            return self.__seguirThread

    def stopThread(self):
        with self.__lock:
            self.__seguirThread = False

    def run(self):
        with self.__lock:
            self.__seguirThread = True
            seguir = self.__seguirThread

        while seguir:
            with self.__lock:
                seguir = self.__seguirThread
            x = 0
            while x < self.__poolingTime:
                seguir = self.threadIsRunning()
                if not seguir:
                    break

                time.sleep(0.01)

                x += 1

                if self.__restartListener is not None and self.__restartListener.restart():
                    x = 0

            if seguir and self.__startListener is not None:
                self.__startListener.start()
