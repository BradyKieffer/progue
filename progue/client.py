import os
from lib import libtcodpy as libtcod
from engine import GameEngine
from utils.render_utils import SCREEN_HEIGHT, SCREEN_WIDTH
from progue.utils.file_management import save_game, load_game


class Client(object):

    def __init__(self):
        self.font_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'assets/terminal12x12_gs_ro.png')
        libtcod.console_set_custom_font(
            self.font_path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    def run(self):
        self.on_run()
        first_run = True
        while not libtcod.console_is_window_closed():
            if not first_run:
                actions = self.engine.update()

                if actions['SAVE']:
                    save_game(game_engine=self.engine, save_dir=self.save_dir)
                    print 'Saved!'

                if actions['QUIT']:
                    break

            first_run = False

    def on_run(self):
        world_name = 'DEBUG'
        
        loaded_attributes = load_game(world_name=world_name, save_dir=self.save_dir)
        loaded_attributes = self.check_loaded_attributes(loaded_attributes)
        self.engine = GameEngine(title='progue', loaded_attributes=loaded_attributes, save_dir=self.save_dir)
        self.engine.init()

    def set_save_dir(self, save_dir):
        self.save_dir = save_dir

    def check_loaded_attributes(self, loaded_attributes):
        loaded = True
        for key in loaded_attributes.keys():
            loaded = loaded_attributes[key] is not None
        
        if loaded:
            return loaded_attributes

        return False