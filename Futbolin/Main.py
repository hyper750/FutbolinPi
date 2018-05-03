import time
from Game import Game
from MotionImplements import LocalGoalSound, VisitorGoalSound, RestartGoalSound, StopGame



if __name__ == "__main__":
    game = Game()
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