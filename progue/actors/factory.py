""" Create actors here """
import random
from jackal import Jackal

class ActorFactory(object):
    def __init__(self, world):
        self.actors = []
        self.world = world

    def make_jackals(self, num):
        for i in xrange(num):
            x = random.randint(0, self.world.width )
            y = random.randint(0, self.world.height)
            self.actors.append(Jackal(x=x, y=y, world=self.world))