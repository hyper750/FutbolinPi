import json
import time
from Game import Game
from GameController import LocalGoalSound, VisitorGoalSound, RestartGoalSound, StopGame, GameController, RestartBoo, StartBoo

if __name__ == "__main__":
    with open(GameController.SETTINGS, "r") as file:
        jsonFile = json.loads(file.read())
        balls = int(jsonFile["balls"])
        localSensor = int(jsonFile["localPin"])
        visitorSensor = int(jsonFile["visitorPin"])
        restartSensor = int(jsonFile["restartPin"])
        stopSensor = int(jsonFile["stopPin"])
        booTime = jsonFile["booSoundTime"]

    game = Game(balls, localSensor, visitorSensor, restartSensor, stopSensor, booTime)
    # When you score a goal
    game.setLocalSensorListener(LocalGoalSound(game))
    game.setVisitorSensorListener(VisitorGoalSound(game))
    game.setRestartSensorListener(RestartGoalSound(game))
    game.setStopSensorListener(StopGame(game))
    game.setRestartBooListener(RestartBoo(game))
    game.setStartBooListener(StartBoo())

    game = Game(balls, localSensor, visitorSensor, restartSensor, stopSensor, booTime)
    # When you score a goal
    game.setLocalSensorListener(LocalGoalSound(game))
    game.setVisitorSensorListener(VisitorGoalSound(game))
    game.setRestartSensorListener(RestartGoalSound(game))
    game.setStopSensorListener(StopGame(game))
    game.setRestartBooListener(RestartBoo(game))
    game.setStartBooListener(StartBoo())

    # Start the game
    game.start()

    #When i push the stop button the python and raspberry stops
    result = ""
    while game.isPlaying():
        if result != game.getResult():
            result = game.getResult()
            print(result)

        time.sleep(0.1)