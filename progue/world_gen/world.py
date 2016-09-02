""" The world we will create """
import world_gen
import math
from progue.world_gen.world_gen import WorldBuilder
from progue.world_gen.chunk import Chunk
from progue.world_gen.chunk_manager import ChunkManager
from progue.utils.actor_constants import PLAYER
from progue.utils.render_utils import *
from progue.debug.logger import log_message, log_endl


class World(object):

    def __init__(self, chunk_dir, name='DEBUG', width=WORLD_WIDTH, height=WORLD_HEIGHT,
                 chunk_width=CHUNK_WIDTH, chunk_height=CHUNK_HEIGHT):

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
            num_chunks_y=num_chunks_y
        )

        self.world_builder = WorldBuilder(
            world_width=width,
            world_height=height,
            chunk_width=chunk_width,
            chunk_height=chunk_height
        )

        self.actors = []
        self.player = None
        self.chunk = None

    def on_new_game(self):
        self.chunk = self.chunk_manager.to_tiles(self.world_builder.generate_world())


    def on_update(self):
        # log_endl()
        # log_message(self.actors)
        if self.update_tiles():
            self.chunk_manager.update_actors(self.actors)
            self.chunk = self.chunk_manager.build_chunk_map(player=self.get_player())
            
            self.actors = self.chunk.actors
            player = self.get_player()
            player.update_coords()
            player.prev_chunk_num = player.curr_chunk_num

            


    def actor_at(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

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
            return self.chunk[chunk_num_y][chunk_num_x].tiles[chunk_y][chunk_x]

        except Exception:
            chunk = self.chunk_manager.get_chunk_from_pos(x=x, y=y)
            return chunk.tiles[chunk_y][chunk_x]

    def update_tiles(self):
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
            self.chunk[chunk_y][chunk_x].actors.append(actor)
            
            """
            log_endl()
            log_message(self.chunk[chunk_y][chunk_x])
            log_message(actor)
            log_endl()
            """
