import threading
from pygame import mixer
import time


class EndMusicEndgif(threading.Thread):
    INSTANCE  = None

    def __init__(self, view):
        threading.Thread.__init__(self)
        self.__lock = threading.Lock()
        self.__seguir = False
        self.__view = view
        self.__visible = False

    def run(self):
        with self.__lock:
            self.__seguir = True
            seguir = self.__seguir

        while seguir:
            with self.__lock:
                visible = self.__visible

            if visible:
                self.__view.visibleGifView(True)
                while mixer.music.get_busy():
                    #print("Waiting music")
                    time.sleep(0.5)
                #print("Acabat musica")
                self.__view.visibleGifView(False)
                with self.__lock:
                    self.__visible = False
            time.sleep(0.1)
            #print("Bucle Endmusic")

            with self.__lock:
                seguir = self.__seguir

        #print("EndMusic acabat")



    def stopThread(self):
        with self.__lock:
            if self.__seguir:
                self.__seguir = False

    def startGif(self):
        with self.__lock:
            self.__visible = True

    @staticmethod
    def getInstance(view):
        if EndMusicEndgif.INSTANCE is None:
            EndMusicEndgif.INSTANCE = EndMusicEndgif(view)
            EndMusicEndgif.INSTANCE.start()

        return EndMusicEndgif.INSTANCE