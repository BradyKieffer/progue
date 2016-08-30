""" The player! """
from ..lib import libtcodpy as libtcod
from actor import Actor

class Player(Actor):

    def __init__(self, x, y, world):
        Actor.__init__(self, x=x, y=y, world=world, glyph='@', fore_color=libtcod.white, back_color=libtcod.black, ai=None)