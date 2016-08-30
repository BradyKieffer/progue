""" The world we will create """
import random
import world_gen
from ..tiles import *


# Maxmimum values for tiles to appear
THRESHOLDS = {
    TILE_WATER: 0.0,
    TILE_SAND: 0.2,
    TILE_GROUND: 0.85,
    TILE_WALL: 1.0 # For now this is unused
}

class World(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.base = 16 #random.randint(0, 255)

        self.raw_map = world_gen.generate_world(self.width, self.height, self.base)
        self.map = self.create_tile_map(self.raw_map)
        self.actors = []

    def tile_num_map(self, num):
        if num < THRESHOLDS[TILE_WATER]:
            return TILES[TILE_WATER]
        
        elif num < THRESHOLDS[TILE_SAND]:
            return TILES[TILE_SAND]

        elif num < THRESHOLDS[TILE_GROUND]:
            return TILES[TILE_GROUND]
        
        else:
            return TILES[TILE_WALL]

    def create_tile_map(self, raw_map):
        res = []
        for j in xrange(len(raw_map)):
            res.append([])
            for i in xrange(len(raw_map[j])):
                res[j].append(self.tile_num_map(raw_map[j][i]))

        return res

    def tile_at(self, x, y):
        return self.map[y][x]

    def in_bounds(self, x, y):
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return True
        return False 

    def actor_at(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None