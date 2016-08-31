""" The first actor to be put into the game """
import random
import copy
from progue.lib import libtcodpy as libtcod
from progue.ai.ai import AI
from progue.utils.action_utils import ACTION_WANDER
from progue.utils.actor_constants import ATTRIBUTES
from progue.actors.actor import Actor
from progue.ai.brain import BrainIdle

class Jackal(Actor):
    def __init__(self, x, y, world, attributes):
        self.attributes = copy.deepcopy(attributes[ATTRIBUTES])
        Actor.__init__(self, x=x, y=y, world=world, attributes=attributes)

class JackalAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor=actor, bored=ACTION_WANDER, brain=[BrainIdle])
        
