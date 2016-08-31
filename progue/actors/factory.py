""" Create actors here """
import random
from collections import defaultdict
from progue.utils.actor_utils import get_actor
from progue.utils.actor_constants import *

class ActorFactory(object):
    def __init__(self, world):
        self.actors = []
        self.world = world

    def make_jackals(self, num):
        x = y = 0
        created_list = []
        for i in xrange(num):
            spawned = False
            while not spawned:
                x = random.randint(0, self.world.width )
                y = random.randint(0, self.world.height)
                spawned = self.spawnable_tile(x, y, created_list)

            attr = get_actor(ACTOR_JACKAL)
            self.actors.append(attr[CLASS](x=x, y=y, world=self.world, attributes=attr))
            created_list.append((x, y))

    def spawnable_tile(self, x, y, created_list):
        tile = self.world.tile_at(x=x, y=y)
        if not tile or (x, y) in created_list:
            return False

        return tile.passable
