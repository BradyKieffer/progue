""" Offload the management of chunks from the world to here """
class ChunkManager(object):
    def __init__(self, chunk_width, chunk_height, load_distance):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.load_distance = load_distance

    def get_chunk_map(self, world):
        pass