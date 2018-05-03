import json
import os
import time

from Music import Music
from Game import Game

class LocalGoalSound(Game.LocalGoal):
    def __init__(self, game):
        Game.LocalGoal.__init__(self, game)
        #Default
        musicFolder = "Music"
        if os.path.exists(Game.SETTINGS_FILE):
            with open(Game.SETTINGS_FILE, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]

        self.__music = Music(musicFolder)

    def motion(self):
        Game.LocalGoal.motion(self)
        print("GOOL local!")
        self.__music.random()

class VisitorGoalSound(Game.VisitorGoal):
    def __init__(self, game):
        Game.VisitorGoal.__init__(self, game)
        #Default
        musicFolder = "Music"
        if os.path.exists(Game.SETTINGS_FILE):
            with open(Game.SETTINGS_FILE, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]

        self.__music = Music(musicFolder)

    def motion(self):
        Game.VisitorGoal.motion(self)
        print("GOOL Visitant!")
        self.__music.random()

class RestartGoalSound(Game.RestartGame):
    def __init__(self, game):
        Game.RestartGame.__init__(self, game)
        #Default
        musicFolder = "Music"
        self.__restartSound = "restart.mp3"
        if os.path.exists(Game.SETTINGS_FILE):
            with open(Game.SETTINGS_FILE, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]
                self.__restartSound = jsonFile["restartSound"]

        self.__music = Music(musicFolder)

    def motion(self):
        Game.RestartGame.motion(self)
        self.__music.play(self.__restartSound)
        print("Restarting score!")

class StopGame(Game.StopGame):
    def __init__(self, game):
        Game.StopGame.__init__(self, game)
        #Default
        musicFolder = "Music"
        self.__stopSound = "restart.mp3"
        if os.path.exists(Game.SETTINGS_FILE):
            with open(Game.SETTINGS_FILE, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]
                self.__stopSound = jsonFile["powerOffSound"]

        self.__music = Music(musicFolder)

    def motion(self):
        Game.StopGame.motion(self)
        self.__music.play(self.__stopSound)
        print("PowerOff raspberry!")
        #W8 to finish the sound
        while self.__music.isPlayingMusic():
            time.sleep(0.8)

        #When the song finish
        os.system("poweroff")