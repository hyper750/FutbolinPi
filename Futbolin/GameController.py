import json
import os
import time
from RestartListener import RestartListener
from Music import Music
from Game import Game
from GraphicInterface import MainWindow


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
            musicFolder = jsonFile["musicFolder"]
            booSound = jsonFile["booSound"]
            booTime = jsonFile["booSoundTime"]
            gifFolder = jsonFile["gifFolder"]

        self.view = MainWindow(gifFolder)

        self.game = Game(balls, localSensor, visitorSensor, restartSensor, stopSensor, musicFolder, booSound, booTime)
        # When you score a goal
        self.game.setLocalSensorListener(LocalGoalGraphic(self.game, self.view))
        self.game.setVisitorSensorListener(VisitorGoalGraphic(self.game, self.view))
        self.game.setRestartSensorListener(RestartGoalSound(self.game))
        self.game.setStopSensorListener(StopGameGraphic(self.game, self.view))
        self.game.setRestartBooListener(RestartBoo(self.game))

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

        self.__music = Music(musicFolder)

    def motion(self):
        finish = self.game.gameFinish()
        Game.LocalGoal.motion(self)
        if not finish:
            print("GOOL local!")
            self.__music.random()

class LocalGoalGraphic(LocalGoalSound):
    def __init__(self, game, view):
        LocalGoalSound.__init__(self, game)
        self.view = view

    def motion(self):
        LocalGoalSound.motion(self)
        #Update view
        self.view.setText(self.game.getResult())


class VisitorGoalSound(Game.VisitorGoal):
    def __init__(self, game):
        Game.VisitorGoal.__init__(self, game)
        #Default
        musicFolder = "Music"
        if os.path.exists(GameController.SETTINGS):
            with open(GameController.SETTINGS, "r") as file:
                jsonFile = json.loads(file.read())
                musicFolder = jsonFile["musicFolder"]

        self.__music = Music(musicFolder)

    def motion(self):
        finish = self.game.gameFinish()
        Game.VisitorGoal.motion(self)
        if not finish:
            print("GOOL Visitant!")
            self.__music.random()


class VisitorGoalGraphic(VisitorGoalSound):
    def __init__(self, game, view):
        VisitorGoalSound.__init__(self, game)
        self.view = view

    def motion(self):
        #Update view
        VisitorGoalSound.motion(self)
        self.view.setText(self.game.getResult())




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
            time.sleep(0.5)

        #When the song finish, poweroff
        #os.system("poweroff")


class StopGameGraphic(StopGame):
    def __init__(self, game, view):
        StopGame.__init__(self, game)
        self.__view = view

    def motion(self):
        StopGame.motion(self)
        self.__view.finishWindow()


class RestartBoo(RestartListener):
    def __init__(self, game):
        self.game = game
        self.result = self.game.getResult()

    def restart(self):
        if self.game.getResult() != self.result:
            self.result = self.game.getResult()
            return True
        return False