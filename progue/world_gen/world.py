""" The world we will create """
import world_gen
from chunk import Chunk
from progue.utils.render_utils import *

class World(object):

    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT, chunk_width=CHUNK_WIDTH, chunk_height=CHUNK_HEIGHT):
        self.width = width
        self.height = height

        self.chunk_width = chunk_width
        self.chunk_height = chunk_height

        self.num_chunks = self.width / self.chunk_width # Assume this is an integer

        self.map = world_gen.generate_world(self.chunk_width, self.chunk_height, self.num_chunks)

        self.create_tile_map()

        self.actors = []
        self.player = None

    def actor_at(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def get_chunk_num(self, x, y):
        chunk_num = int(y / self.chunk_height)

        return max(0, min(chunk_num, len(self.map)-1))

    def to_chunk_coords(self, x, y):
        (chunk_x, chunk_y) = (x % self.chunk_width, y % self.chunk_height)

        return (chunk_x, chunk_y)

    def create_tile_map(self):
        for chunk in self.map:
            chunk.create_tile_map()

    def tile_at(self, x, y):
        chunk_num = self.get_chunk_num(x, y)
        (chunk_x, chunk_y) = self.to_chunk_coords(x, y)
        chunk = self.map[chunk_num]
        return chunk.map[chunk_y][chunk_x]

    def in_bounds(self, x, y):
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return True
        return False