from os import listdir
from os.path import isfile, join, exists
from random import randint
from pygame import mixer



class Music:
    MUSIC_EXTENSIONS = ("mp3", "wav", "ogg", "oga", "mogg", "wma")
    RANDOM_FOLDER = "Random"

    def __init__(self, musicFolder):
        self.__musicFolder = musicFolder
        self.__randomMusic = [obj for obj in listdir(self.__musicFolder + "/" + self.RANDOM_FOLDER)
                              if isfile(join(self.__musicFolder + "/" + self.RANDOM_FOLDER, obj)) and obj.__str__().split(".")[-1] in self.MUSIC_EXTENSIONS]
        mixer.init()


    def random(self):
        if len(self.__randomMusic) > 0:
            randomNum = randint(0, len(self.__randomMusic)-1)
            randomMusic = self.__randomMusic[randomNum]
            mixer.music.load(self.__musicFolder + "/" + self.RANDOM_FOLDER + "/" + randomMusic)
            mixer.music.play()

    def play(self, sound):
        if exists(self.__musicFolder + "/" + sound):
            mixer.music.load(self.__musicFolder + "/" + sound)
            mixer.music.play()

    def isPlayingMusic(self):
        return mixer.music.get_busy()