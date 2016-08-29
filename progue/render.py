""" For now put all rendering code in here """
from lib import libtcodpy as libtcod


class Renderer(object):

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def render_world(self, world):
        for j in xrange(world.height):
            for i in xrange(world.width):
                tile = world.tile_at(i, j)
                self.render_tile(i, j, tile)

    def render_tile(self, x, y, tile):
        libtcod.console_put_char(0, x, y, tile.glyph)
        libtcod.console_set_char_foreground(0, x, y, tile.fore_color)
        libtcod.console_set_char_background(
            0, x, y, tile.back_color, flag=libtcod.BKGND_SET)

    def render_player(self, x, y):
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, x, y, '@', libtcod.BKGND_NONE)
