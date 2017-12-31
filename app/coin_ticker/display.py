import requests
import logging
from PIL import ImageFont
from waveshare_lib import epd2in13b
from data_source import Data

COLORED = 1
UNCOLORED = 0

class Display(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.__epd = epd2in13b.EPD()
        self.__epd.init()
        self.__frame_black = []
        self.__frame_red = []

    def reset_frames(self):
        self.__frame_black = [0xFF] * (self.__epd.width * self.__epd.height / 8)
        self.__frame_red = [0xFF] * (self.__epd.width * self.__epd.height / 8)

    def draw_gain_number(self, data):
        gain = data[-1].gain()
        gain_str = '{:.0f}%'.format(gain)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 55)
        x = 0
        y = 10
        self.__epd.draw_string_at(self.__frame_black, x, y, gain_str, font, COLORED)

    def draw_gain_chart(self, data):
        gains = map(lambda x: x.gain(), data)
        norm = [float(i)/max(gains) for i in gains]
        self.draw_bar_chart(norm)

    def draw_bar_chart(self, points):
        point_count = len(points)
        if point_count < 1:
            return

        point_width = epd2in13b.EPD_HEIGHT / point_count
        chart_height = epd2in13b.EPD_WIDTH - 60
        
        for y in range (0, epd2in13b.EPD_HEIGHT):
            div = int(y / point_width)
            index = point_count - 1 - min(div, point_count - 1)
            value = points[index]
                
            line_height = int(value * chart_height)
            for x in range(epd2in13b.EPD_WIDTH, epd2in13b.EPD_WIDTH - line_height, -1):
                self.__epd.set_pixel(self.__frame_red, x, y, COLORED)

    def draw_content(self, data):
        self.draw_gain_chart(data)
        self.draw_gain_number(data)

    def update(self, data):
        self.reset_frames()
        self.draw_content(data)
        self.__epd.display_frame(self.__frame_black, self.__frame_red)
