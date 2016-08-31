""" Create actors here """
import random
from collections import defaultdict
from progue.utils.actor_utils import get_actor
from progue.utils.actor_constants import *

class ActorFactory(object):
    def __init__(self, world):
        self.world = world
        self.to_make = []
        self.prep_actors()

    def prep_jackals(self):
        self.prep_actor(num=100, label=ACTOR_JACKAL)

    def prep_player(self):
        self.prep_actor(num=1, label=PLAYER)

    def prep_actors(self):
        self.prep_jackals()
        self.prep_player()


    def prep_actor(self, num, label):
        x = y = 0
        for i in xrange(num):
            prepped = False
            while not prepped:
                x = random.randint(0, self.world.width-1 )
                y = random.randint(0, self.world.height-1)
                prepped = self.world.spawnable_tile(x, y)

            self.to_make.append(self.ActorToMake(x=x, y=y, label=label))

    def make_actors(self):
        actors = []
        for actor in self.to_make:
            label = actor.label
            attr = get_actor(label)
            actors.append(attr[CLASS](x=actor.x, y=actor.y, world=self.world, attributes=attr))

        self.world.store_actors(actors)

    class ActorToMake(object):
        def __init__(self, x, y, label):
            self.x = x
            self.y = y
            self.label = label