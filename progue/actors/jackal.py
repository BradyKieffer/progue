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
        AI.__init__(self, actor=actor, fov=10.0)

    def on_update(self):
        mx = my = 0
        player = self.actor.world.player
        if self.actor.distance_to(player) <= self.fov:
            if player.x > self.actor.x:
                mx = 1
            elif player.x < self.actor.x:
                mx = -1

            if player.y > self.actor.y:
                my = 1
            elif player.y < self.actor.y:
                my = -1

        else:
            prob_x = random.random()
            prob_y = random.random()

            if prob_x > 0.80:
                if prob_x > 0.9:
                    mx = 1
                else:
                    mx = -1

            if prob_y > 0.80:
                if prob_y > 0.9:
                    my = 1
                else:
                    my = -1

        self.actor.move_to(mx=mx, my=my)

