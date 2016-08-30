""" General actor class """
import math
from ..lib import libtcodpy as libtcod

class Actor(object):
    def __init__(self, x, y, world, glyph, fore_color, back_color, ai):
        self.x = x
        self.y = y
        self.world = world
        self.glyph = glyph
        self.fore_color = fore_color
        self.back_color = back_color
        self.ai = ai

    def on_update(self):
        if self.ai is not None:
            self.ai.on_update()

    def on_render(self, renderer_in):
        (x, y) = renderer_in.to_camera_coords(self.x, self.y)

        libtcod.console_put_char(0, x, y, self.glyph)
        libtcod.console_set_char_foreground(0, x, y, self.fore_color)
        libtcod.console_set_char_background(0, x, y, self.back_color, flag=libtcod.BKGND_SET)

    def move_to(self, mx, my):
        new_x = self.x + mx
        new_y = self.y + my

        if new_x < 0 or new_x > self.world.width:
            new_x = 0

        if new_y < 0 or new_y > self.world.height:
            new_y = 0
        
        if not self.world.actor_at(x=new_x, y=new_y):
            tile = self.world.tile_at(x=new_x, y=new_y)
            if tile is not None and tile.passable:
                self.x = new_x
                self.y = new_y
                return True

        return False

    def distance_to(self, other):
        """ Compute the disctance to another actor """
        rel_x = self.x - other.x
        rel_y = self.y - other.y

        return math.sqrt(rel_x*rel_x + rel_y*rel_y)