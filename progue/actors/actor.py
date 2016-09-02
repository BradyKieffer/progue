""" General actor class """
import math
import copy
from uuid import uuid1
from collections import defaultdict
from progue.lib import libtcodpy as libtcod
from progue.utils.actor_constants import *
from progue.debug.logger import log_message


class Actor(object):

    def __init__(self, x, y, world, attributes):

        self.__id = uuid1(id(self)).bytes

        self.name = attributes[NAME]
        self.x = x
        self.y = y


        self.world = world
        self.curr_chunk_num = self.prev_chunk_num = self.world.chunk_manager.get_chunk_num(self.x, self.y)

        self.glyph = attributes[GLYPH]
        self.fore_color = attributes[FORE_COLOR]
        self.back_color = attributes[BACK_COLOR]
        self.attributes = copy.deepcopy(attributes[ATTRIBUTES])

        if attributes[AI] is not None:
            self.ai = attributes[AI](self)
        else:
            self.ai = None

    def __repr__(self):
        return '<{cls}:{x}>'.format(cls=self.__class__.__name__, x=(self.x, self.y))

    def __eq__(self, other):
        return self.__id == other.get_unique_id()

    def get_unique_id(self):
        return self.__id

    def check_current_pos(self):
        """ Keep a record of the actors chunk """
        curr_chunk_num = self.world.chunk_manager.get_chunk_num(self.x, self.y)
        if self.curr_chunk_num != curr_chunk_num:
            self.prev_chunk_num = self.curr_chunk_num
            self.curr_chunk_num = curr_chunk_num

    def on_update(self):
        if self.ai is not None:
            self.ai.on_update()

        # To help with storing actors
        self.check_current_pos()

    def on_render(self, renderer_in):
        (x, y) = renderer_in.to_camera_coords(self.x, self.y)

        if x is not None and y is not None:
            libtcod.console_put_char(0, x, y, self.glyph)
            libtcod.console_set_char_foreground(0, x, y, self.fore_color)
            libtcod.console_set_char_background(
                0, x, y, self.back_color, flag=libtcod.BKGND_SET)

    def move_to(self, mx, my):

        new_x = self.x + mx
        new_y = self.y + my

        if new_x < 0 or new_x > self.world.width - 1:
            new_x = self.x

        if new_y < 0 or new_y > self.world.height - 1:
            new_y = self.y

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

        return math.sqrt(rel_x * rel_x + rel_y * rel_y)

    def update_chunk(self):
        return self.prev_chunk_num != self.curr_chunk_num
