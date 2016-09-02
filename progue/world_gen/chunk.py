import random
import math
from progue.tiles import *
from progue.utils.file_management import load_chunk, save_chunk
from progue.debug.logger import log_message, log_endl

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


class ChunkManager(object):
    """ Offload the management of chunks from the world to here """

    def __init__(self, save_dir, world_name, chunk_width, chunk_height, num_chunks_x, num_chunks_y, load_distance):
        self.save_dir = save_dir
        self.world_name = world_name

        self.num_chunks_x = num_chunks_x
        self.num_chunks_y = num_chunks_y

        self.chunk_width = chunk_width
        self.chunk_height = chunk_height

        self.load_distance = load_distance

    def to_tiles(self, raw_map):
        """ Take a raw map and convert it to a tile map of chunks """
        for chunks in raw_map:
            for chunk in chunks:
                chunk.create_tile_map()

        return raw_map

    def build_chunk_map(self, player):
        """ When called this will build a chunk map around the player """
        chunk_map = []
        (player_chunk_num_x, player_chunk_num_y) = self.get_actor_chunk_num(player)
        (x_start, x_end, y_start, y_end) = self.compute_chunk_bounds(player_chunk_num_x, player_chunk_num_y)

        for y in xrange(y_start, y_end):
            chunk_map.append([])
            for x in xrange(x_start, x_end):
                chunk_map[y].append(load_chunk(
                    save_dir=self.save_dir, world_name=self.world_name, x=x, y=y))

        return chunk_map

    def compute_chunk_bounds(self, x, y):
        x_start = max(0, min(self.num_chunks_x - self.load_distance,
                             x - self.load_distance))
        x_end = max(0, min(self.num_chunks_x - self.load_distance,
                           x + self.load_distance))

        y_start = max(0, min(self.num_chunks_y - self.load_distance,
                             y - self.load_distance))
        y_end = max(0, min(self.num_chunks_y - self.load_distance,
                           y + self.load_distance))

        return (x_start, x_end, y_start, y_end)

    def save_chunk_map(self, chunk_map):
        for chunks in chunk_map:
            for chunk in chunks:
                save_chunk(chunk=chunk, world_name=self.world_name,
                           save_dir=self.save_dir)

    def get_actor_chunk_num(self, actor):
        return self.get_chunk_num(x=actor.x, y=actor.y)

    def to_chunk_coords(self, x, y):
        (chunk_x, chunk_y) = (x % self.chunk_width, y % self.chunk_height)

        return (chunk_x, chunk_y)

    def assign_actor_to_chunk(self, actor):
        chunk = self.get_actor_chunk(actor)
        if actor in chunk.actors:
            chunk.remove_actor(actor)

        chunk.actors.append(actor)
        save_chunk(chunk=chunk, world_name=self.world_name, save_dir=self.save_dir)

    def actor_chunk_coords(self, actor):
        (chunk_x, chunk_y) = self.get_chunk_num(actor.x, actor.y)
        (x, y) = self.to_chunk_coords(actor.x, actor.y)

        return (chunk_x, chunk_y, x, y)
    # Old funcs ##############################################################
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

    def get_player_chunk(self):
        return self.get_actor_chunk(self.get_player())

    def deload_chunks(self):
        for chunks in self.map:
            for chunk in chunks:
                save_chunk(chunk=chunk, world_name=self.world_name,
                           save_dir=self.save_dir)

    def update_chunk_actors(self):

        for actor in self.actors:
            chunk = self.get_actor_chunk(actor)
            if not (actor in chunk.actors):
                chunk.actors.append(actor)


    def load_actors(self):
        """ Get actors from currently loaded chunks """
        self.actors = []
        for chunks in self.map:
            for chunk in chunks:
                self.actors += chunk.actors

    def __load_chunk(self, x, y):
        # log_message('Loading chunk at: {}'.format((x, y)))
        return load_chunk(save_dir=self.save_dir, world_name=self.world_name, x=x, y=y)

    # This is a mess
    def blah(self):
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
                save_chunk(chunk=old_chunk, world_name=self.world_name,
                           save_dir=self.save_dir)
                save_chunk(chunk=new_chunk, world_name=self.world_name,
                           save_dir=self.save_dir)
                actor.prev_chunk_num = actor.curr_chunk_num
