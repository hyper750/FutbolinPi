import json
import os
from MotionListener import MotionListener
from MotionSensor import MotionSensor


class Game:
    SETTINGS_FILE = "settings.json"
    def __init__(self):
        #Default 7 balls, without sensors
        self.__balls = 7
        self.__localSensor = None
        self.__visitorSensor = None
        self.__restartSensor = None
        self.__stopSensor = None

        self.__playing = False

        #Goals
        self.__localScore = 0
        self.__visitorScore = 0

        #Importing settings
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r") as file:
                jsonFile = json.loads(file.read())
                self.__balls = int(jsonFile["balls"])
                self.__localSensor = MotionSensor(int(jsonFile["localPin"]))
                self.__visitorSensor = MotionSensor(int(jsonFile["visitorPin"]))
                self.__restartSensor = MotionSensor(int(jsonFile["restartPin"]))
                self.__stopSensor = MotionSensor(int(jsonFile["stopPin"]))

        else:
            print(self.SETTINGS_FILE + " NOT FOUND")

        #Default listeners

        # What to do when a goal is scored
        self.setLocalSensorListener(Game.LocalGoal(self))
        self.setVisitorSensorListener(Game.VisitorGoal(self))

        # What to do when you restart the game
        self.setRestartSensorListener(Game.RestartGame(self))

        # What to do when you stop the game
        self.setStopSensorListener(Game.StopGame(self))

    def start(self):
        if self.__localSensor is None or self.__visitorSensor is None or self.__restartSensor is None or self.__stopSensor is None:
            print("First you need to initiate all the sensors")
            return

        self.__localSensor.start()
        self.__visitorSensor.start()
        self.__restartSensor.start()
        self.__stopSensor.start()
        self.__playing = True

    def stop(self):
        self.__localSensor.stopThread()
        self.__visitorSensor.stopThread()
        self.__restartSensor.stopThread()
        self.__stopSensor.stopThread()
        self.__playing = False

    def restart(self):
        self.__visitorScore = 0
        self.__localScore = 0

    def isPlaying(self):
        return self.__playing

    def addLocalScore(self):
        self.__localScore += 1

    def addVisitorScore(self):
        self.__visitorScore += 1

    def getLocalScore(self):
        return self.__localScore

    def getVisitorScore(self):
        return self.__visitorScore

    def setLocalSensorListener(self, listener):
        self.__localSensor.setMotionListener(listener)

    def setVisitorSensorListener(self, listener):
        self.__visitorSensor.setMotionListener(listener)

    def setRestartSensorListener(self, listener):
        self.__restartSensor.setMotionListener(listener)

    def setStopSensorListener(self, listener):
        self.__stopSensor.setMotionListener(listener)

    class LocalGoal(MotionListener):
        def __init__(self, game):
            self.__game = game

        def motion(self):
            self.__game.addLocalScore()

    class VisitorGoal(MotionListener):
        def __init__(self, game):
            self.__game = game

        def motion(self):
            self.__game.addVisitorScore()

    class RestartGame(MotionListener):
        def __init__(self, game):
            self.__game = game

        def motion(self):
            self.__game.restart()

    class StopGame(MotionListener):
        def __init__(self, game):
            self.__game = game
        def motion(self):
            self.__game.stop()