""" Implement a tile class and then create a list of tiles """
import random
from lib import libtcodpy as libtcod
from utils.console_utils import *

TILE_VACUUM = 'WATER'
TILE_GROUND = 'GROUND'
TILE_WALL = 'WALL'
TILE_SAND = 'SAND'
TILE_DEBUG = 'DEBUG'
TILE_NOT_VISIBLE = 'NOT_VISIBLE' # Used for computing fov

# Maxmimum values for tiles to appear
THRESHOLDS = {
    TILE_VACUUM: 0.0,
    TILE_SAND: 0.2,
    TILE_GROUND: 0.75,
    TILE_WALL: 1.0  # For now this is unused
}

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
    TILE_GROUND:      Tile(material=TILE_GROUND,      glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.amber,       back_color=libtcod.black,       passable=True ),
    TILE_WALL:        Tile(material=TILE_WALL,        glyph='#',                  fore_color=libtcod.light_amber, back_color=libtcod.dark_amber,       passable=False),
    TILE_SAND:        Tile(material=TILE_SAND,        glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.dark_amber,  back_color=libtcod.black,       passable=True ),
    TILE_VACUUM: {
        '*':          Tile(material=TILE_VACUUM,      glyph='*',                  fore_color=libtcod.white,       back_color=libtcod.black,       passable=False),
        ' ':          Tile(material=TILE_VACUUM,      glyph=' ',                  fore_color=libtcod.white,       back_color=libtcod.black,       passable=False),
        '.':          Tile(material=TILE_VACUUM,      glyph='.',    fore_color=libtcod.white,       back_color=libtcod.black,                     passable=False)
    },
    TILE_NOT_VISIBLE: Tile(material=TILE_NOT_VISIBLE, glyph=SPARSE_DOTTED_SQUARE, fore_color=libtcod.gray,        back_color=libtcod.darker_gray, passable=True ),

}

def tile_num_map(num):
        if num < THRESHOLDS[TILE_VACUUM]:
            val = random.random()
            if val < 0.05:
                if val < 0.02:
                    return TILES[TILE_VACUUM]['*']
                else:
                    return TILES[TILE_VACUUM]['.']
            else:
                return TILES[TILE_VACUUM][' ']

        elif num < THRESHOLDS[TILE_SAND]:
            return TILES[TILE_SAND]

        elif num < THRESHOLDS[TILE_GROUND]:
            return TILES[TILE_GROUND]

        else:
            return TILES[TILE_WALL]
