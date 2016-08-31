from noise import snoise2
from chunk import Chunk
import random 
DEFAULT_LACUNARITY = 2.0
DEFAULT_GAIN = 0.65
DEFAULT_OCTAVES = 7


def generate_world(world, width, height, chunk_width, chunk_height):
    res = [[Chunk(x=i, y=j, width=chunk_width, height=chunk_height) for i in xrange(width)] for j in xrange(height)]

    for j in xrange(height):
        for i in xrange(width):
            (x, y) = world.to_chunk_coords(x=i, y=j)

            pos_x = int(i / chunk_width )
            pos_y = int(j / chunk_height)

            chunk = res[pos_y][pos_x]
            chunk.raw_map[y][x] = fractal(x=i, y=j, hgrid=width, base=255)

    return res


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
