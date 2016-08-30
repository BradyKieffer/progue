from noise import snoise2

DEFAULT_LACUNARITY = 2.0
DEFAULT_GAIN = 0.65
DEFAULT_OCTAVES = 7

def generate_world(width, height, base):
    world = []
    octaves = 7
    freq = 16.0 * octaves

    for j in xrange(height):
        world.append([])
        for i in xrange(width):
            world[j].append(fractal(x=i, y=j, hgrid=width, base=base))

    return world

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