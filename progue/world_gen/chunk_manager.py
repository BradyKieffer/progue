import math
from progue.world_gen.chunk import Chunk
from progue.utils.file_management import load_chunk, save_chunk
from progue.debug.logger import log_message, log_endl

class ChunkManager(object):
    """ Offload the management of chunks from the world to here """

    def __init__(self, save_dir, world_name, chunk_width, chunk_height, num_chunks_x, num_chunks_y):
        self.save_dir = save_dir
        self.world_name = world_name

        self.num_chunks_x = num_chunks_x
        self.num_chunks_y = num_chunks_y

        self.chunk_width = chunk_width
        self.chunk_height = chunk_height

        self.offset = (None, None)

        self.loaded_chunk = None

    def to_tiles(self, raw_map):
        """ Take a raw map and convert it to a tile map of chunks """
        for chunks in raw_map:
            for chunk in chunks:
                chunk.create_tile_map()

        return raw_map

    def build_chunk_map(self, player):
        """ When called this will build a chunk map around the player """
        (offset_x, offset_y) = self.calc_chunk_offset(player)

        (x, y) = self.get_actor_chunk_num(player)
        self.loaded_chunk = self.__load_chunk(x=x, y=y)
        
        log_message(self.loaded_chunk)

        return self.loaded_chunk

    def compute_chunk_bounds(self, x, y):
        x_start = max(0, x - self.load_distance)
        x_end = min(self.num_chunks_x, x + self.load_distance + 1)
        y_start = max(0, y - self.load_distance)
        y_end = min(self.num_chunks_y, y + self.load_distance + 1)

        return (x_start, x_end, y_start, y_end)

    def save_chunk_map(self, chunk_map):
        for chunks in chunk_map:
            for chunk in chunks:
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
        offset_x = max(0, x - 1)
        offset_y = max(0, y - 1)
        return (offset_x, offset_y)

    def update_actors(self, actors):
        for actor in actors:
            if actor.update_chunk():
                prev_chunk = self.get_chunk_from_num(actor.prev_chunk_num)
                prev_chunk.remove_actor(actor)
                self.assign_actor_to_chunk(actor)

    def load_actors(self, x, y):
        """ Get actors from currently loaded chunks """
        return self.__load_chunk(x=x, y=y).actors


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