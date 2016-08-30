""" The first actor to be put into the game """
import random
from ..lib import libtcodpy as libtcod
from actor import Actor
from ai import AI

class Jackal(Actor):
    def __init__(self, x, y, world):
        Actor.__init__(self, x=x, y=y, world=world, glyph='j', fore_color=libtcod.sepia, back_color=libtcod.black, ai=JackalAI(self))

class JackalAI(AI):
    def __init__(self, actor):
        AI.__init__(self, actor=actor)

    def on_update(self):
        prob_x = random.random()
        prob_y = random.random()

        mx = my = 0
        if prob_x > 0.25:
            if prob_x > 0.75:
                mx = 1
            else:
                mx = -1

        if prob_y > 0.25:
            if prob_y > 0.75:
                my = 1
            else:
                my = -1

        self.actor.move_to(mx=-1, my=-1)

