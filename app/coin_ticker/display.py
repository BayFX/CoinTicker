import requests
from PIL import ImageFont
from waveshare_lib import epd2in13b
from data_source import Data

COLORED = 1
UNCOLORED = 0

class Display(object):
    def __init__(self):
        self.__epd = epd2in13b.EPD()
        self.__epd.init()
        self.__frame_black = []
        self.__frame_red = []

    def reset_frames(self):
        self.__frame_black = [0xFF] * (self.__epd.width * self.__epd.height / 8)
        self.__frame_red = [0xFF] * (self.__epd.width * self.__epd.height / 8)

    def draw_content(self, data):
        gain = data.gain()
        gain_str = '{:.1f}%'.format(gain)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 55)
        self.__epd.draw_string_at(self.__frame_black, 0, 20, gain_str, font, COLORED)

    def update(self, data):
        self.reset_frames()
        self.draw_content(data)
        self.__epd.display_frame(self.__frame_black, self.__frame_red)
