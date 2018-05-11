import gi
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import os
from random import randint
import threading


class RandomGif(threading.Thread):
    EXTENSIONS = ["gif"]
    INSTANCE = None

    def __init__(self, gifFolder, totalGif):
        threading.Thread.__init__(self)
        self.__gifFolder = gifFolder
        self.__lock = threading.Lock()
        self.__totalGifsACarregar = totalGif
        self.__seguir = False
        if os.path.exists(self.__gifFolder):
            #GdkPixbuf.PixbufAnimation.new_from_file(os.path.join(self.__gifFolder, gif))

            self.__gifFiles = [os.path.join(self.__gifFolder, gif) for gif in os.listdir(self.__gifFolder)
                                      if os.path.isfile(os.path.join(self.__gifFolder, gif)) and
                                      gif.__str__().split(".")[-1] in self.EXTENSIONS]
            self.__gifPixbuf = []


    def run(self):
        with self.__lock:
            self.__seguir = True
            seguir = self.__seguir

        while seguir:
            #print("Bucle")
            with self.__lock:
                seguir = self.__seguir
                pixBufLen = len(self.__gifPixbuf)

            #print("Tamany PixbufBuffer " + str(pixBufLen))
            while pixBufLen < self.__totalGifsACarregar and seguir:
                #print("Carregant")
                randomNumber = randint(0, len(self.__gifFiles) - 1)
                pxbuf = GdkPixbuf.PixbufAnimation.new_from_file( self.__gifFiles[randomNumber])
                with self.__lock:
                    #print("Loading")
                    self.__gifPixbuf.append(pxbuf)
                    #print("Loaded")
                pixBufLen += 1

                with self.__lock:
                    seguir = self.__seguir


            time.sleep(0.1)

        #print("Random gif acabat")

    def stopThread(self):
        with self.__lock:
            if self.__seguir:
                self.__seguir = False


    def random(self):
        with self.__lock:
            if len(self.__gifPixbuf) > 0:
                randomPix = self.__gifPixbuf.pop(0)
                return randomPix

        return None

    @staticmethod
    def getInstance(gifFolder):
        if RandomGif.INSTANCE is None:
            RandomGif.INSTANCE = RandomGif(gifFolder, 5)
            RandomGif.INSTANCE.start()

        return RandomGif.INSTANCE