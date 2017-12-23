from time import sleep
from display import Display

class Updater(object):
    def __init__(self):
        self.__display = Display()
        self.__running = False

    def start(self):
        if self.__running:
            pass
        self.__running = True
        while self.__running:
            self.__display.update()
            sleep(20)

    def stop(self):
        self.__running = False
