import threading
from SongPooling import SongPooling
from MotionListener import MotionListener
from MotionSensor import MotionSensor


class Game(threading.Thread):
    def __init__(self, balls, localPin, visitorPin, restartPin, stopPin, folder, booSound, booTime):
        threading.Thread.__init__(self)
        #Default 7 balls, without sensors
        self.__balls = balls
        self.__localSensor = MotionSensor(localPin)
        self.__visitorSensor = MotionSensor(visitorPin)
        self.__restartSensor = MotionSensor(restartPin)
        self.__stopSensor = MotionSensor(stopPin)
        self.__jeer = SongPooling(folder, booSound, booTime)

        self.__playing = False

        #Goals
        self.__localScore = 0
        self.__visitorScore = 0

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
        self.__jeer.start()
        self.__playing = True

    def stop(self):
        self.__localSensor.stopThread()
        self.__visitorSensor.stopThread()
        self.__restartSensor.stopThread()
        self.__stopSensor.stopThread()
        self.__jeer.stopThread()
        self.__playing = False

    def restart(self):
        self.__visitorScore = 0
        self.__localScore = 0

    def isPlaying(self):
        return self.__playing

    def gameFinish(self):
        return (self.__visitorScore + self.__localScore) == self.__balls

    def addLocalScore(self):
        if not self.gameFinish():
            self.__localScore += 1

    def addVisitorScore(self):
        if not self.gameFinish():
            self.__visitorScore += 1

    def getResult(self):
        return str(self.__localScore) + " - " + str(self.__visitorScore)

    def getLocalScore(self):
        return self.__localScore

    def getVisitorScore(self):
        return self.__visitorScore

    def getTotalBalls(self):
        return self.__balls

    def setLocalSensorListener(self, listener):
        self.__localSensor.setMotionListener(listener)

    def setVisitorSensorListener(self, listener):
        self.__visitorSensor.setMotionListener(listener)

    def setRestartSensorListener(self, listener):
        self.__restartSensor.setMotionListener(listener)

    def setStopSensorListener(self, listener):
        self.__stopSensor.setMotionListener(listener)

    def setRestartBooListener(self, listener):
        self.__jeer.setRestartListener(listener)

    class LocalGoal(MotionListener):
        def __init__(self, game):
            self.game = game

        def motion(self):
            self.game.addLocalScore()

    class VisitorGoal(MotionListener):
        def __init__(self, game):
            self.game = game

        def motion(self):
            self.game.addVisitorScore()

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