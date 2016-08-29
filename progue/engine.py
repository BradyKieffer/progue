from world_gen.world import World
from lib import libtcodpy as libtcod
from render import Renderer


class GameEngine(object):

    def __init__(self, screen_width, screen_height, title):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title

        self.playerx = self.playery = 0
        self.renderer = Renderer(screen_width=self.screen_width, screen_height=self.screen_height)
        self.world = World(width=self.screen_width, height=self.screen_height)

    def init(self):
        libtcod.console_init_root(
            self.screen_width, self.screen_height, self.title, False)

        self.playerx = self.screen_width / 2
        self.playery = self.screen_height / 2

    def update(self):
        """ Main game loop will go here """
        # 1. Logic

        # 2. Render
        self.render()

        # 3. Player Input
        exit = self.handle_keys()

        return exit

    def render(self):
        self.renderer.render_world(self.world)
        self.renderer.render_player(self.playerx, self.playery)
        libtcod.console_flush()

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)  # turn-based

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        elif key.vk == libtcod.KEY_ESCAPE:
            return True  # exit game

        libtcod.console_put_char(
            0, self.playerx, self.playery, ' ', libtcod.BKGND_NONE)

        # movement keys
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            self.playery -= 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            self.playery += 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            self.playerx -= 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            self.playerx += 1
