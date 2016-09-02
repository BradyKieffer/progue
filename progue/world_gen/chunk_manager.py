import math
from progue.world_gen.chunk import Chunk
from progue.utils.file_management import load_chunk, save_chunk
from progue.debug.logger import log_message, log_endl

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

        self.offset = (None, None)

        self.loaded_chunks = self.__blank_map()

    def to_tiles(self, raw_map):
        """ Take a raw map and convert it to a tile map of chunks """
        for chunks in raw_map:
            for chunk in chunks:
                chunk.create_tile_map()

        return raw_map

    def __blank_map(self):
        size = 3 * self.load_distance +  2 * (self.load_distance - 1)
        return [[None for i in xrange(size)] for j in xrange(size)]

    def build_chunk_map(self, player):
        """ When called this will build a chunk map around the player """
        self.loaded_chunks = self.__blank_map()
        (offset_x, offset_y) = self.calc_chunk_offset(player)

        (player_chunk_num_x, player_chunk_num_y) = self.get_actor_chunk_num(player)
        
        (x_start, x_end, y_start, y_end) = self.compute_chunk_bounds(player_chunk_num_x, player_chunk_num_y)

        log_message((player_chunk_num_x, player_chunk_num_y))
        log_message((x_start, x_end, y_start, y_end))

        for j in xrange(y_start, y_end):
            y = j - offset_y 
            for i in xrange(x_start, x_end):
                x = i - offset_x
                if (i, j) != self.loaded_chunks[y][x]:
                    self.loaded_chunks[y][x] = load_chunk(save_dir=self.save_dir, world_name=self.world_name, x=i, y=j)

        log_message(self.loaded_chunks)
        return self.loaded_chunks

    def compute_chunk_bounds(self, x, y):
        x_start = max(0, x - self.load_distance)
        x_end = min(self.num_chunks_x, x + self.load_distance + 1)
        y_start = max(0, y - self.load_distance)
        y_end = min(self.num_chunks_y, y + self.load_distance + 1)

        return (x_start, x_end, y_start, y_end)

    def save_chunk_map(self, chunk_map):
        for chunks in chunk_map:
            for chunk in chunks:
                if isinstance(chunk, Chunk):
                    self.save_chunk(chunk=chunk)

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
        self.save_chunk(chunk)

    def save_chunk(self, chunk):
        save_chunk(chunk=chunk, world_name=self.world_name, save_dir=self.save_dir)

    def actor_chunk_coords(self, actor):
        (chunk_x, chunk_y) = self.get_chunk_num(actor.x, actor.y)
        (x, y) = self.to_chunk_coords(actor.x, actor.y)

        return (chunk_x, chunk_y, x, y)

    def calc_chunk_offset(self, player):
        (x, y) = self.get_actor_chunk_num(player)
        offset_x = max(0, x - self.load_distance)
        offset_y = max(0, y - self.load_distance)
        return (offset_x, offset_y)

    def update_actors(self, actors):
        for actor in actors:
            if actor.update_chunk():
                prev_chunk = self.get_chunk_from_num(actor.prev_chunk_num)
                prev_chunk.remove_actor(actor)
                self.assign_actor_to_chunk(actor)

    def load_actors(self):
        """ Get actors from currently loaded chunks """
        actors = []
        for chunks in self.loaded_chunks:
            for chunk in chunks:
                if isinstance(chunk, Chunk):
                    actors.extend(chunk.actors)

        return actors

    def save_actors(self, actors):
        """ Saves actors to their chunks """
        for actor in actors:
            old_chunk = self.get_chunk_from_num(actor.prev_chunk_num)
            new_chunk = self.get_chunk_from_num(actor.curr_chunk_num)

            old_chunk.remove_actor(actor)
            new_chunk.add_actor(actor)

            self.save_chunk(old_chunk)
            self.save_chunk(new_chunk)

            actor.prev_chunk_num = actor.curr_chunk_num


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

    def __load_chunk(self, x, y):
        # log_message('Loading chunk at: {}'.format((x, y)))
        return load_chunk(save_dir=self.save_dir, world_name=self.world_name, x=x, y=y)