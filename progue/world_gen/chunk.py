import random
from progue.tiles import *


# Maxmimum values for tiles to appear
THRESHOLDS = {
    TILE_WATER: 0.0,
    TILE_SAND: 0.2,
    TILE_GROUND: 0.75,
    TILE_WALL: 1.0  # For now this is unused
}


class Chunk(object):

    def __init__(self, x, y, width, height, debug=False):
        self.x = x
        self.y = y
        self.num = (x, y)
        self.width = width
        self.height = height
        self.raw_map = [[0 for i in xrange(width)] for j in xrange(height)]
        self.tiles = [[0 for i in xrange(width)] for j in xrange(height)]

        self.actors = []
        self.debug = debug

    def __repr__(self):
        return '<{x} {y}>'.format(x=self.__class__.__name__, y=(self.x, self.y))

    @property
    def name(self):
        return 'chunk{x}{y}'.format(x=self.x, y=self.y)

    def tile_num_map(self, num):
        if num < THRESHOLDS[TILE_WATER]:
            return TILES[TILE_WATER][random.randint(0, len(TILES[TILE_WATER]) - 1)]

        elif num < THRESHOLDS[TILE_SAND]:
            return TILES[TILE_SAND]

        elif num < THRESHOLDS[TILE_GROUND]:
            return TILES[TILE_GROUND]

        else:
            return TILES[TILE_WALL]

    def create_tile_map(self):
        height = len(self.raw_map)
        width = len(self.raw_map[0])
        for j in xrange(height):
            for i in xrange(width):
                if self.debug:
                    if i == 0 or i == width - 1 or j == 0 or j == height - 1:
                        self.tiles[j][i] = TILES[TILE_DEBUG]
                else:
                    self.tiles[j][i] = self.tile_num_map(self.raw_map[j][i])

    def tile_at(self, x, y):
        if self.in_bounds(x, y):
            return self.tiles[y][x]
        return None

    def in_bounds(self, x, y):
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return True
        return False

    def remove_actor(self, actor):
        self.actors.remove(actor)

    def add_actor(self, actor):
        if actor in self.actors:
            self.remove_actor(actor)

        self.actors.append(actor)