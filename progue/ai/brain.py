""" Functions that feed into a pipeline to modify functions """
import random
from progue.utils.action_utils import ACTION_WANDER, ACTION_IDLE, ACTION_MOVE
from progue.utils.actor_constants import *


class Brain(object):

    def __init__(self, actor):
        self.actor = actor

    def filter_action(self, action):
        return action


class BrainIdle(Brain):

    def __init__(self, actor):
        Brain.__init__(self, actor=actor)
        rng = self.actor.attributes[ATTRIBUTE_IDLE][RANGE]
        self.percent_idle = max(min(rng[1], random.random()), rng[0])

    def filter_action(self, action):
        if random.random() > self.percent_idle:
            return action
        else:
            return ACTION_IDLE
