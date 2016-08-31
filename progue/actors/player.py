""" The player! """
from ..lib import libtcodpy as libtcod
from actor import Actor

class Player(Actor):

    def __init__(self, x, y, world, attributes):
        Actor.__init__(self, x=x, y=y, world=world, attributes=attributes)