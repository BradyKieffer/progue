from noise import snoise2
from chunk import Chunk
import random 
DEFAULT_LACUNARITY = 2.0
DEFAULT_GAIN = 0.65
DEFAULT_OCTAVES = 7


def generate_world(width, height, chunk_num):
    world = []

    for num in xrange(chunk_num):
        chunk = build_chunk(Chunk(num=num, width=width, height=height))
        world.append(chunk)

    return world


def build_chunk(chunk):
    for j in xrange(chunk.height):
        chunk.raw_map.append([])

        for i in xrange(chunk.width):
            chunk.raw_map[j].append(
                fractal(
                    x=i,
                    y=j,
                    base=random.randint(0, 255),
                    hgrid=chunk.width
                )
            )
    return chunk


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
