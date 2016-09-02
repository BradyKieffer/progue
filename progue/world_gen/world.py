""" The world we will create """
import world_gen
import math
from progue.world_gen.world_gen import WorldBuilder
from progue.world_gen.chunk import Chunk, ChunkManager
from progue.utils.actor_constants import PLAYER
from progue.utils.render_utils import *
from progue.debug.logger import log_message, log_endl


class World(object):

    def __init__(self, chunk_dir, name='DEBUG', width=WORLD_WIDTH, height=WORLD_HEIGHT,
                 chunk_width=CHUNK_WIDTH, chunk_height=CHUNK_HEIGHT, chunk_load_dist=CHUNK_LOAD_DISTANCE):

        self.name = name
        self.width = width
        self.height = height

        num_chunks_x = self.width / chunk_width
        num_chunks_y = self.height / chunk_height

        self.chunk_manager = ChunkManager(
            save_dir=chunk_dir,
            world_name=self.name,
            chunk_width=chunk_width,
            chunk_height=chunk_height,
            num_chunks_x=num_chunks_x,
            num_chunks_y=num_chunks_y,
            load_distance=chunk_load_dist
        )

        self.world_builder = WorldBuilder(
            world_width=width,
            world_height=height,
            chunk_width=chunk_width,
            chunk_height=chunk_height
        )

        self.actors = []
        self.player = None

    def on_new_game(self):
        self.tiles = self.chunk_manager.to_tiles(self.world_builder.generate_world())
        
    def on_update(self):
            # log_endl()
            # log_message('Updating render map')
        # if self.update_render_map():
        self.tiles = self.chunk_manager.build_chunk_map(player=self.get_player())

    def actor_at(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def get_render_map(self):
        # Want to get rid of this
        player_chunk = self.get_player_chunk()

        load_dist = self.chunk_load_dist
        x_start = max(0, player_chunk.x - load_dist)
        x_end = min(self.num_chunks_x, player_chunk.x + load_dist)
        y_start = max(0, player_chunk.y - load_dist)
        y_end = min(self.num_chunks_y, player_chunk.y + load_dist)

        self.deload_chunks()

        return self.new_render_map(x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end)

    def new_render_map(self, x_start, x_end, y_start, y_end):
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
        (chunk_x, chunk_y) = self.chunk_manager.to_chunk_coords(x, y)
        (chunk_num_x, chunk_num_y) = self.chunk_manager.get_chunk_num(x, y)
        
        try:
            return self.tiles[chunk_num_y][chunk_num_x].tiles[chunk_y][chunk_x]

        except Exception:
            chunk = self.chunk_manager.get_chunk_from_pos(x=x, y=y)
            return chunk.tiles[chunk_y][chunk_x]

    def update_render_map(self):
        if self.get_player().update_chunk():
            return True
        return False

    def get_player(self):
        for actor in self.actors:
            if actor.name == PLAYER:
                return actor

    def store_actors(self, actors):
        for actor in actors:
            (chunk_x, chunk_y, x, y) = self.chunk_manager.actor_chunk_coords(actor)
            self.tiles[chunk_y][chunk_x].actors.append(actor)

    def get_loaded_actors(self):
        actors = []
        for chunks in self.tiles:
            for chunk in chunks:
                actors.extend(chunk.actors)
        return actors