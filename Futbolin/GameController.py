import json
import os
import time
from pygame import mixer

from Pooling import RestartListener, StartListener
from RandomGif import RandomGif
from Music import Music
from Game import Game
from GraphicInterface import MainWindow
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class GameController:
    SETTINGS = "settings.json"

    def __init__(self):
        with open(GameController.SETTINGS, "r") as file:
            jsonFile = json.loads(file.read())
            balls = int(jsonFile["balls"])
            localSensor = int(jsonFile["localPin"])
            visitorSensor = int(jsonFile["visitorPin"])
            restartSensor = int(jsonFile["restartPin"])
            stopSensor = int(jsonFile["stopPin"])
            booTime = jsonFile["booSoundTime"]



        self.view = MainWindow()

        self.game = Game(balls, localSensor, visitorSensor, restartSensor, stopSensor, booTime)
        # When you score a goal
        self.game.setLocalSensorListener(LocalGoalGraphic(self.game, self.view))
        self.game.setVisitorSensorListener(VisitorGoalGraphic(self.game, self.view))
        self.game.setRestartSensorListener(RestartGoalGraphic(self.game, self.view))
        self.game.setStopSensorListener(StopGameGraphic(self.game, self.view))
        self.game.setRestartBooListener(RestartBoo(self.game))
        self.game.setStartBooListener(StartBoo())

        # Start the game
        self.game.start()



class LocalGoalSound(Game.LocalGoal):
    def __init__(self, game):
        Game.LocalGoal.__init__(self, game)
        # Default
        musicFolder = "Music"
        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]

        self.music = Music(musicFolder)

    def motion(self):
        Game.LocalGoal.motion(self)
        finish = self.game.gameFinish()
        if not finish:
            print("GOOL local!")
            self.music.random()

class LocalGoalGraphic(LocalGoalSound):
    def __init__(self, game, view):
        LocalGoalSound.__init__(self, game)
        self.__view = view

        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
                jsonFile = json.loads(file.read())
                gifFolder = jsonFile["gifFolder"]
        else:
            gifFolder = "Gif"
        self.__randomGif = RandomGif(gifFolder)

    def motion(self):
        LocalGoalSound.motion(self)
        # Update view
        self.__view.setText(self.game.getResult())
        self.__view.setGif(self.__randomGif.random())
        self.__view.visibleGifView(True)
        while self.music.isPlayingMusic():
            time.sleep(0.1)
        self.__view.visibleGifView(False)


class VisitorGoalSound(Game.VisitorGoal):
    def __init__(self, game):
        Game.VisitorGoal.__init__(self, game)
        #Default
        musicFolder = "Music"
        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]

        self.music = Music(musicFolder)

    def motion(self):
        Game.VisitorGoal.motion(self)
        finish = self.game.gameFinish()
        if not finish:
            print("GOOL Visitant!")
            self.music.random()


class VisitorGoalGraphic(VisitorGoalSound):
    def __init__(self, game, view):
        VisitorGoalSound.__init__(self, game)
        self.__view = view

        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
                jsonFile = json.loads(file.read())
                gifFolder = jsonFile["gifFolder"]
        else:
            gifFolder = "Gif"
        self.__randomGif = RandomGif(gifFolder)

    def motion(self):
        #Update view
        VisitorGoalSound.motion(self)
        self.__view.setText(self.game.getResult())
        self.__view.setGif(self.__randomGif.random())
        self.__view.visibleGifView(True)
        while self.music.isPlayingMusic():
            time.sleep(0.1)
        self.__view.visibleGifView(False)



class RestartGoalSound(Game.RestartGame):
    def __init__(self, game):
        Game.RestartGame.__init__(self, game)
        #Default
        musicFolder = "Music"
        self.__restartSound = "restart.mp3"
        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]
                self.__restartSound = jsonFile["restartSound"]

        self.__music = Music(musicFolder)

    def motion(self):
        Game.RestartGame.motion(self)
        self.__music.play(self.__restartSound)
        print("Restarting score!")

class RestartGoalGraphic(RestartGoalSound):
    def __init__(self, game, view):
        RestartGoalSound.__init__(self, game)
        self.__view = view

    def motion(self):
        RestartGoalSound.motion(self)
        self.__view.setText("0 - 0")



class StopGame(Game.StopGame):
    def __init__(self, game):
        Game.StopGame.__init__(self, game)
        #Default
        musicFolder = "Music"
        self.__stopSound = "restart.mp3"
        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
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
            time.sleep(0.1)

        #When the song finish, poweroff
        #os.system("poweroff")


class StopGameGraphic(StopGame):
    def __init__(self, game, view):
        StopGame.__init__(self, game)
        self.__view = view

    def motion(self):
        StopGame.motion(self)
        Gtk.main_quit()


class RestartBoo(RestartListener):
    def __init__(self, game):
        self.__game = game
        self.__result = self.__game.getResult()

    def restart(self):
        if self.__game.getResult() != self.__result or self.__game.gameFinish():
            self.__result = self.__game.getResult()
            #print("Reiniciar")
            return True
        return False

class StartBoo(StartListener):
    def __init__(self):
        with open(GameController.SETTINGS, "r") as file:
            jsonFile = json.loads(file.read())
            self.__song = jsonFile["booSound"]
            folder = jsonFile["musicFolder"]
        self.__music = Music(folder)

    def start(self):
        self.__music.play(self.__song)