""" The world we will create """
import world_gen
import math
from chunk import Chunk
from progue.utils.actor_constants import PLAYER
from progue.utils.render_utils import *
from progue.debug.logger import log_message, log_endl
from progue.utils.file_management import load_chunk, save_chunk


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

    def get_chunk_num(self, x, y):
        """ get a chunk number (x, y) from given coordinates """
        pos_x = int(math.floor(x / self.chunk_width))
        pos_y = int(math.floor(y / self.chunk_height))
        return (pos_x, pos_y)

    def get_chunk_from_num(self, chunk_num):
        x = chunk_num[0]
        y = chunk_num[1]
        return self.__load_chunk(x, y)

    def get_chunk_from_pos(self, x, y):

        (pos_x, pos_y) = self.get_chunk_num(x, y)
        return self.__load_chunk(pos_x, pos_y)

    def get_player(self):
        for actor in self.actors:
            if actor.name == PLAYER:
                return actor

    def get_player_chunk(self):
        return self.get_actor_chunk(self.get_player())

    def get_render_map(self):
        player_chunk = self.get_player_chunk()

        load_dist = self.chunk_load_dist
        x_start = max(0, player_chunk.x - load_dist)
        x_end = min(self.num_chunks_x, player_chunk.x + load_dist)
        y_start = max(0, player_chunk.y - load_dist)
        y_end = min(self.num_chunks_y, player_chunk.y + load_dist)

        self.deload_chunks()

        return self.new_render_map(x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end)

    def deload_chunks(self):
        for chunks in self.map:
            for chunk in chunks:
                save_chunk(chunk=chunk, world_name=self.name,
                           save_dir=self.chunk_dir)

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

    def on_update(self):
            # log_endl()
            # log_message('Updating render map')
        if self.update_render_map():
            # self.fuck_this_shit()
            # self.player = self.get_player()
            self.map = self.get_render_map()

    def fuck_this_shit(self):
        for actor in self.actors:
            if actor.update_chunk():
                old_chunk = self.get_chunk_from_num(actor.prev_chunk_num)
                new_chunk = self.get_chunk_from_num(actor.curr_chunk_num)

                # log_message('World actors:        {}'.format(self.actors))
                # log_message('Old chunk to remove: {}'.format(actor.prev_chunk_num))
                # log_message('New chunk to add:    {}'.format(actor.curr_chunk_num))
                # log_endl()
                # log_message('Old chunk actors:    {}'.format(old_chunk.actors))
                # log_message('New chunk actors:    {}'.format(new_chunk.actors))
                # log_endl()

                # try:
                old_chunk.remove_actor(actor)
                # except Exception:
                    # log_message('Current Actor: {}'.format(actor))
                    # log_message('Old Chunk: {}'.format(old_chunk))
                    # log_message('Trying to remove from: {}'.format(old_chunk.actors))
                    # raise ValueError()

                new_chunk.actors.append(actor)
                # log_message('After update')
                # log_message('Old chunk actors:    {}'.format(old_chunk.actors))
                # log_message('New chunk actors:    {}'.format(new_chunk.actors))
                # log_endl()
                save_chunk(chunk=old_chunk, world_name=self.name,
                           save_dir=self.chunk_dir)
                save_chunk(chunk=new_chunk, world_name=self.name,
                           save_dir=self.chunk_dir)
                actor.prev_chunk_num = actor.curr_chunk_num

    def update_chunk_actors(self):

        for actor in self.actors:
            chunk = self.get_actor_chunk(actor)
            if not (actor in chunk.actors):
                chunk.actors.append(actor)

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

    def store_actors(self, actors):
        for actor in actors:
            chunk = self.get_actor_chunk(actor)
            if actor in chunk.actors:
                chunk.remove_actor(actor)

            chunk.actors.append(actor)
            save_chunk(chunk=chunk, world_name=self.name,
                       save_dir=self.chunk_dir)

    def load_actors(self):
        """ Get actors from currently loaded chunks """
        self.actors = []
        for chunks in self.map:
            for chunk in chunks:
                self.actors += chunk.actors

    def __load_chunk(self, x, y):
        try:
            (offset_x, offset_y) = (self.map[0][0].x, self.map[0][0].y)
            return self.map[y - offset_y][x - offset_x]
        except IndexError:

            log_message('Loading chunk at: {}'.format((x, y)))
            return load_chunk(save_dir=self.chunk_dir, world_name=self.name, x=x, y=y)

    def update_render_map(self):
        if self.get_player().update_chunk():
            return True
        return False
