import json
import time
from Game import Game
from MotionImplements import LocalGoalSound, VisitorGoalSound, RestartGoalSound, StopGame

SETTINGS = "settings.json"

if __name__ == "__main__":
    with open(SETTINGS, "r") as file:
        jsonFile = json.loads(file.read())
        balls = int(jsonFile["balls"])
        localSensor = int(jsonFile["localPin"])
        visitorSensor = int(jsonFile["visitorPin"])
        restartSensor = int(jsonFile["restartPin"])
        stopSensor = int(jsonFile["stopPin"])
    game = Game(balls, localSensor, visitorSensor, restartSensor, stopSensor)
    #When you score a goal
    game.setLocalSensorListener(LocalGoalSound(game))
    game.setVisitorSensorListener(VisitorGoalSound(game))
    game.setRestartSensorListener(RestartGoalSound(game))
    game.setStopSensorListener(StopGame(game))

    #Start the game
    game.start()

    #When i push the stop button the python and raspberry stops
    result = ""
    while game.isPlaying():
        if result != game.getResult():
            result = game.getResult()
            print(result)

        time.sleep(0.1)