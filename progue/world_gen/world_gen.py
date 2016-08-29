from simplexnoise.noise import SimplexNoise, normalize

def generate_world(width, height):
    world = []

    sn = SimplexNoise(num_octaves=7, persistence=0.1, dimensions=2)

    for j in xrange(height):
        world.append([])
        for i in xrange(width):
            world[j].append(sn.fractal(x=i, y=j, hgrid=width))

    return world