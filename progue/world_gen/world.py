""" The world we will create """
import world_gen
import math
from chunk import Chunk
from progue.utils.actor_constants import PLAYER
from progue.utils.render_utils import *
from progue.debug.logger import log_message
from progue.utils.file_management import load_chunk


class World(object):

    def __init__(self, chunk_dir, name='DEBUG', width=WORLD_WIDTH, height=WORLD_HEIGHT,
                 chunk_width=CHUNK_WIDTH, chunk_height=CHUNK_HEIGHT, chunk_load_dist=CHUNK_LOAD_DISTANCE):

        self.name = name
        self.width = width
        self.height = height

        self.chunk_width = chunk_width
        self.chunk_height = chunk_height

        # Assume these are integers
        self.num_chunks_x = self.width / self.chunk_width
        self.num_chunks_y = self.height / self.chunk_height

        self.chunk_load_dist = chunk_load_dist

        self.chunk_dir = chunk_dir

        self.map = None
        world_gen.generate_world(
            world=self,
            width=self.width,
            height=self.height,
            chunk_height=self.chunk_height,
            chunk_width=self.chunk_width,
            num_chunks_x=self.num_chunks_x,
            num_chunks_y=self.num_chunks_y
        )

        self.prev_player_chunk = (None, None)

        for chunks in self.map:
            for chunk in chunks:
                chunk.create_tile_map()

        self.actors = []
        self.player = None

    def actor_at(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def get_actor_chunk(self, actor):
        return self.get_chunk_from_pos(actor.x, actor.y)

    def get_chunk_from_pos(self, x, y):
        pos_x = int(math.floor(x / self.chunk_width))
        pos_y = int(math.floor(y / self.chunk_height))

        try:
            return self.map[pos_y][pos_x]
        except IndexError:
            return load_chunk(save_dir=self.chunk_dir, world_name=self.name, x=pos_x, y=pos_y)

    def get_player(self):
        for actor in self.actors:
            if actor.name == PLAYER:
                return actor

    def get_player_chunk(self):
        return self.get_actor_chunk(self.get_player())

    def in_bounds(self, x, y):
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return True
        return False

    def spawnable_tile(self, x, y):
        tile = self.tile_at(x=x, y=y)
        if not tile or self.actor_at(x=x, y=y):
            return False

        return tile.passable

    def tile_at(self, x, y):
        (chunk_x, chunk_y) = self.to_chunk_coords(x, y)
        chunk = self.get_chunk_from_pos(x=x, y=y)
        return chunk.map[chunk_y][chunk_x]

    def to_chunk_coords(self, x, y):
        (chunk_x, chunk_y) = (x % self.chunk_width, y % self.chunk_height)

        return (chunk_x, chunk_y)

    def on_update(self):
        if self.update_render_map():
            self.purge_chunk_actors()
            self.store_actors(self.actors)
            self.load_actors()

            # Needs to be last 
            self.map = self.get_render_map()

    def get_render_map(self):
        player_chunk = self.get_player_chunk()

        load_dist = self.chunk_load_dist
        x_start = max(0, player_chunk.x - load_dist)
        x_end = min(self.num_chunks_x, player_chunk.x + load_dist)
        y_start = max(0, player_chunk.y - load_dist)
        y_end = min(self.num_chunks_y, player_chunk.y + load_dist)

        return [
            [
                load_chunk(
                    save_dir=self.chunk_dir,
                    world_name=self.name,
                    x=i,
                    y=j
                )
                for i in xrange(x_start, x_end)
            ] for j in xrange(y_start, y_end)
        ]

    def update_render_map(self):
        player_chunk = self.get_player_chunk()
        coords = (player_chunk.x, player_chunk.y)
        
        if self.prev_player_chunk != coords:
            self.prev_player_chunk = coords
            return True
        return False

    def purge_chunk_actors(self):
        for chunks in self.map:
            for chunk in chunks:
                chunk.actors = []

    def load_actors(self):
        self.actors = []
        for chunks in self.map:
            for chunk in chunks:
                self.actors += chunk.actors

    def store_actors(self, actors):
        for actor in actors:
            chunk = self.get_chunk_from_pos(actor.x, actor.y)
            chunk.actors.append(actor)
