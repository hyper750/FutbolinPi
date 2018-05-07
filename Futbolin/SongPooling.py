import threading
import time
from RestartListener import RestartListener
from Music import Music


class SongPooling(threading.Thread):
    def __init__(self, folder, song, poolingTime):
        threading.Thread.__init__(self)
        self.__music = Music(folder)
        self.__song = song
        self.__seguirThread = False
        self.__restartListener = None
        self.poolingTime = poolingTime * 100

    def setRestartListener(self, listener):
        if isinstance(listener, RestartListener):
            self.__restartListener = listener

    def threadIsRunning(self):
        return self.__seguirThread

    def stopThread(self):
        self.__seguirThread = False

    def run(self):
        self.__seguirThread = True

        while self.__seguirThread:
            x = 0
            while x < self.poolingTime:
                if not self.__seguirThread:
                    break

                time.sleep(0.01)

                x += 1

                if self.__restartListener is not None and self.__restartListener.restart():
                    x = 0

            if self.__seguirThread:
                self.__music.play(self.__song)