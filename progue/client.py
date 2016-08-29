import os
from lib import libtcodpy as libtcod
from engine import GameEngine

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

class Client(object):
    def __init__(self):
        self.font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/terminal8x8_aa_as.png')
        libtcod.console_set_custom_font(self.font_path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
        self.engine = GameEngine(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, title='progue')


    def run(self):
        self.engine.init()
        while not libtcod.console_is_window_closed():
            exit = self.engine.update()
            if exit:
                break