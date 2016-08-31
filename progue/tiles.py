""" Implement a tile class and then create a list of tiles """
from lib import libtcodpy as libtcod
from utils.console_utils import *

TILE_WATER = 'WATER'
TILE_GROUND = 'GROUND'
TILE_WALL = 'WALL'
TILE_SAND = 'SAND'
TILE_DEBUG = 'DEBUG'


class Tile(object):

    def __init__(self, glyph, fore_color, back_color, passable):
        self.glyph = glyph
        self.fore_color = fore_color
        self.back_color = back_color
        self.passable = passable

TILES = {
    TILE_DEBUG:  Tile(glyph=' ',                  fore_color=libtcod.black,       back_color=libtcod.black,       passable=True ),
    TILE_GROUND: Tile(glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.dark_green,  back_color=libtcod.black,       passable=True ),
    TILE_WALL:   Tile(glyph='#',                  fore_color=libtcod.dark_gray,   back_color=libtcod.black,       passable=True),
    TILE_SAND:   Tile(glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.light_sepia, back_color=libtcod.black,       passable=True ),
    TILE_WATER: [
                 Tile(glyph='~',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                 Tile(glyph=' ',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                 Tile(glyph=' ',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                 Tile(glyph=' ',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                 Tile(glyph=APPROX_EQUAL_SIGN,    fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
    ],
}
