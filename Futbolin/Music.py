from os import listdir
from os.path import isfile, join
from random import randint
from pygame import mixer



class Music:
    MUSIC_EXTENSIONS = ("mp3", "wav", "ogg", "oga", "mogg", "wma")
    def __init__(self, musicFolder):
        self.__musicFolder = musicFolder
        self.__musicFiles = [obj for obj in listdir(self.__musicFolder)
                             if isfile(join(self.__musicFolder, obj)) and obj.__str__().split(".")[-1] in self.MUSIC_EXTENSIONS]
        mixer.init()


    def random(self):
        if len(self.__musicFiles) > 0:

            musicFiles = [obj for obj in listdir(self.__musicFolder)
                          if isfile(join(self.__musicFolder, obj)) and obj.__str__().split(".")[-1] in self.MUSIC_EXTENSIONS]
            randomNum = randint(0, len(musicFiles)-1)
            randomMusic = musicFiles[randomNum]
            mixer.music.load(self.__musicFolder + "/" + randomMusic)
            mixer.music.play()

    def play(self, sound):
        if sound in self.__musicFiles:
            mixer.music.load(self.__musicFolder + "/" + sound)
            mixer.music.play()

    def isPlayingMusic(self):
        return mixer.music.get_busy()