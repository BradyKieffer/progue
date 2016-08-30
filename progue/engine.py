import random
from world_gen.world import World
from lib import libtcodpy as libtcod
from render import Renderer
from actors.player import Player
from actors.factory import ActorFactory
from input_proc import InputProcessor
from utils.render_utils import CAMERA_HEIGHT, CAMERA_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_HEIGHT, WORLD_WIDTH


class GameEngine(object):

    def __init__(self, title):
        self.title = title
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.renderer = Renderer(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            world_width=WORLD_WIDTH,
            world_height=WORLD_HEIGHT,
            camera_width=CAMERA_WIDTH,
            camera_height=CAMERA_HEIGHT
        )

        self.world = World(width=WORLD_WIDTH, height=WORLD_HEIGHT)
        
        self.player = Player(
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2,
            world=self.world
        )

        self.inp_proc = InputProcessor()

        self.factory = ActorFactory(world=self.world)
        self.factory.make_jackals(num=100)

    def init(self):
        libtcod.console_init_root(
            self.screen_width,
            self.screen_height,
            self.title,
            False
        )
        self.world.player = self.player

    def update(self):
        """ Main game loop will go here """
        # 1. Logic
        for actor in self.factory.actors:
            actor.on_update()

        self.world.actors = self.factory.actors
        self.world.actors.append(self.player)
        # 2. Render
        self.render()

        # 3. Player Input
        actions = self.inp_proc.handle_keys()

        if actions['MOVE']['mx'] != 0 or actions['MOVE']['my'] != 0:
            self.player.move_to(mx=actions['MOVE']['mx'], my=actions['MOVE']['my'])

        return actions['QUIT']

    def render(self):
        self.renderer.move_camera(self.player.x, self.player.y)
        self.renderer.render_world(self.world)
        self.render_actors(self.factory.actors)
        self.renderer.render_player(self.player)
        libtcod.console_flush()

    def render_actors(self, actors):
        for actor in actors:
            actor.on_render(self.renderer)
