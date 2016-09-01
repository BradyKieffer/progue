""" For now put all rendering code in here """
import math
from lib import libtcodpy as libtcod
from progue.utils.render_utils import *
from progue.debug.logger import log_message


class Renderer(object):

    def __init__(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, world_width=WORLD_WIDTH, world_height=WORLD_HEIGHT, camera_width=CAMERA_WIDTH, camera_height=CAMERA_HEIGHT):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.world_width = world_width
        self.world_height = world_height

        self.camera_width = camera_width
        self.camera_height = camera_height

        self.camera_x = camera_width / 2
        self.camera_y = camera_height / 2

    def render_world(self, world):
        for chunks in world.map:
            for chunk in chunks:
                y = chunk.y * chunk.height
                x = chunk.x * chunk.width
                self.render_chunk(x, y, chunk)

    def render_chunk(self, x, y, chunk):
        for j in xrange(chunk.height):
            for i in xrange(chunk.width):
                (pos_x, pos_y) = self.to_camera_coords(target_x=x + i, target_y=y + j) 
                if (pos_x, pos_y) is not None:
                    tile = chunk.tile_at(i, j)
                    self.render_tile(pos_x, pos_y, tile)


    def __render_world(self, world):
        for j in xrange(self.camera_height):
            y = j + self.camera_y
            for i in xrange(self.camera_width):
                x = i + self.camera_x

                tile = world.tile_at(x, y)
                self.render_tile(i, j, tile)

    def render_tile(self, x, y, tile):
        libtcod.console_put_char(0, x, y, tile.glyph)
        libtcod.console_set_char_foreground(0, x, y, tile.fore_color)
        libtcod.console_set_char_background(
            0, x, y, tile.back_color, flag=libtcod.BKGND_SET)

    def move_camera(self, target_x, target_y):
        """ Centers the viewport on a given object """
        x = target_x - self.camera_width / 2
        y = target_y - self.camera_height / 2

        x = max(0, min(x, self.world_width - self.camera_width))
        y = max(0, min(y, self.world_height - self.camera_height))

        (self.camera_x, self.camera_y) = (x, y)

    def to_camera_coords(self, target_x, target_y):
        """ Move coordinates to camera space """
        (x, y) = (target_x - self.camera_x, target_y - self.camera_y)

        if x < 0 or y < 0 or x > self.camera_width or y > self.camera_height:
            return (None, None)

        return (x, y)
