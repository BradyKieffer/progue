import random
import sys 
from noise import snoise2
from chunk import Chunk
from progue.debug.logger import log_call, log_endl, log_message
DEFAULT_LACUNARITY = 2.0
DEFAULT_GAIN = 0.65
DEFAULT_OCTAVES = 7


@log_call
def generate_world(world, width, height, chunk_width, chunk_height, num_chunks_x, num_chunks_y):
    res = [[Chunk(x=i, y=j, width=chunk_width, height=chunk_height, debug=True) for i in xrange(num_chunks_x)] for j in xrange(num_chunks_y)]

    log_message(res[0][0].name)
    base = random.randint(-chunk_width, chunk_width)
    for j in xrange(height):
        for i in xrange(width):
            (x, y) = world.to_chunk_coords(x=i, y=j)

            pos_x = int(i / chunk_width )
            pos_y = int(j / chunk_height)

            chunk = res[pos_y][pos_x]
            chunk.raw_map[y][x] = fractal(x=i, y=j, hgrid=width, base=base)

    log_message('Created {x} chunks.'.format(x=num_chunks_x*num_chunks_y))
    log_message('Chunk size: {x}'.format(x=chunk_width))
    world.map = res


def fractal(x, y, hgrid, base, num_octaves=DEFAULT_OCTAVES, lacunarity=DEFAULT_LACUNARITY, gain=DEFAULT_GAIN):
    """ A more refined approach but has a much slower run time """
    noise = []
    frequency = 1.0 / hgrid
    amplitude = gain

    for i in xrange(num_octaves):
        noise.append(
            snoise2(
                x=x * frequency,
                y=y * frequency,
                base=base
            ) * amplitude
        )

        frequency *= lacunarity
        amplitude *= gain

    return sum(noise)
