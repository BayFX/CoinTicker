from time import sleep
from display import Display
from data_source import DataSource

class Updater(object):
    def __init__(self, config):
        self.__data_source = DataSource(config)
        self.__display = Display()
        self.__running = False

    def start(self):
        if self.__running:
            pass
        self.__running = True
        while self.__running:
            data = self.__data_source.get()
            self.__display.update(data)
            sleep(60 * 30)

    def stop(self):
        self.__running = False
