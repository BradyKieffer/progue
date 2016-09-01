import random
from lib import libtcodpy as libtcod
from world_gen.world import World
from render import Renderer
from actors.player import Player
from actors.factory import ActorFactory
from input_proc import InputProcessor
from utils.render_utils import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.actor_utils import get_actor
from utils.actor_constants import *
from progue.debug.logger import log_call, log_message, log_endl
from progue.utils.file_management import save_chunks


class GameEngine(object):

    def __init__(self, title, save_dir, loaded_attributes):

        self.title = title
        self.world = None
        self.factory = None
        self.save_dir = save_dir

        self.render_map = []
        self.renderer = Renderer()

        if loaded_attributes == False:
            self.generate_new_game()
        else:
            self.get_loaded_game(loaded_attributes)

        self.player = self.world.get_player()
        self.inp_proc = InputProcessor()

    def init(self):
        libtcod.console_init_root(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.title,
            False
        )
        self.world.load_actors()        
        self.player = self.world.get_player()
        self.print_game_info()


    def generate_new_game(self):
        self.world = World(chunk_dir=self.save_dir)
        self.factory = ActorFactory(world=self.world)
        self.factory.make_actors()
        save_chunks(world=self.world, save_dir=self.save_dir)

    def get_loaded_game(self, loaded_attributes):
        self.world = loaded_attributes['World']
        self.world.actors = loaded_attributes['Actors']
        self.world.store_actors(self.world.actors)
        self.factory = ActorFactory(world=self.world)


    def update(self):
        """ Main game loop will go here """
        # Debug message

        # Checks loaded chunks etc 
        self.world.on_update()

        # 1. Render
        self.render()

        # 2. Player Input
        actions = self.inp_proc.handle_keys()

        if actions['MOVE']['mx'] != 0 or actions['MOVE']['my'] != 0:
            self.player.move_to(mx=actions['MOVE']['mx'], my=actions['MOVE']['my'])

        # 3. Logic
        if actions['UPDATE_LOGIC'] == True:
            for actor in self.world.actors:
                actor.on_update()

        return actions

    def render(self):
        self.renderer.move_camera(self.player.x, self.player.y)
        self.renderer.render_world(self.world)
        self.render_actors(self.world.actors)
        libtcod.console_flush()

    def render_actors(self, actors):
        for actor in actors:
            actor.on_render(self.renderer)

    @log_call
    def print_game_info(self):
        log_message('World {name}'.format(name=self.world.name))
        log_message('\t Size:       {x}'.format(
            x=(self.world.width, self.world.height)))
        log_message('\t Chunks:     {x}'.format(
            x=self.world.num_chunks_x * self.world.num_chunks_y))
        log_message('\t Chunk Size: {x}'.format(x=self.world.chunk_width))
        log_message('\t Actors:     {x}'.format(x=len(self.world.actors)))
        log_endl()
        log_message('Player Data:')
        log_message('\t Position:   {x}'.format(x=(self.world.get_player().x, self.world.get_player().y)))
        log_message('\t Attributes: {x}'.format(x=self.world.get_player().attributes))
