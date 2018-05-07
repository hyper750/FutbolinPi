import gpio
import threading
import time
from MotionListener import MotionListener


class MotionSensor(threading.Thread):
    POLLING_TIME = 0.01
    #Una vegada sa configuracio
    gpio.setmode(gpio.BCM)
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.__pin = pin
        self.setup()
        self.__seguirThread = False
        self.__motionListener = None

    def setup(self):
        gpio.setup(self.__pin, gpio.IN)

    def cleanUp(self):
        gpio.cleanup(self.__pin)

    def motion(self):
        return gpio.input(self.__pin)

    def __del__(self):
        self.cleanUp()

    def __str__(self):
        return "Motion sensor pin " + str(self.__pin)

    def setMotionListener(self, listener):
        if isinstance(listener, MotionListener):
            self.__motionListener = listener

    def threadIsRunning(self):
        return self.__seguirThread

    def stopThread(self):
        self.__seguirThread = False

    def run(self):
        self.__seguirThread = True
        flag = False
        while self.__seguirThread:
            if self.motion():
                if not flag and self.__motionListener is not None:
                    self.__motionListener.motion()
                    flag = True
            else:
                flag = False

            time.sleep(self.POLLING_TIME)