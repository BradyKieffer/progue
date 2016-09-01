""" Implement a tile class and then create a list of tiles """
from lib import libtcodpy as libtcod
from utils.console_utils import *

TILE_WATER = 'WATER'
TILE_GROUND = 'GROUND'
TILE_WALL = 'WALL'
TILE_SAND = 'SAND'
TILE_DEBUG = 'DEBUG'
TILE_NOT_VISIBLE = 'NOT_VISIBLE' # Used for computing fov


class Tile(object):

    def __init__(self, material, glyph, fore_color, back_color, passable):
        self.material = material
        self.glyph = glyph
        self.fore_color = fore_color
        self.back_color = back_color
        self.passable = passable

    def __repr__(self):
        return '<Tile:{x}>'.format(x=self.material)

TILES = {
    TILE_DEBUG:       Tile(material=TILE_DEBUG,       glyph=' ',                  fore_color=libtcod.black,       back_color=libtcod.black,       passable=True ),
    TILE_GROUND:      Tile(material=TILE_GROUND,      glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.dark_green,  back_color=libtcod.black,       passable=True ),
    TILE_WALL:        Tile(material=TILE_WALL,        glyph='#',                  fore_color=libtcod.dark_gray,   back_color=libtcod.black,       passable=True ),
    TILE_SAND:        Tile(material=TILE_SAND,        glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.light_sepia, back_color=libtcod.black,       passable=True ),
    TILE_WATER: [
                      Tile(material=TILE_WATER,       glyph='~',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                      Tile(material=TILE_WATER,       glyph=' ',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                      Tile(material=TILE_WATER,       glyph=' ',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                      Tile(material=TILE_WATER,       glyph=' ',                  fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
                      Tile(material=TILE_WATER,       glyph=APPROX_EQUAL_SIGN,    fore_color=libtcod.blue,        back_color=libtcod.darker_blue, passable=True),
    ],
    TILE_NOT_VISIBLE: Tile(material=TILE_NOT_VISIBLE, glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.gray, back_color=libtcod.darker_gray,        passable=True ),

}
