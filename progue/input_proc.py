""" Handle key input """
from lib import libtcodpy as libtcod


class InputProcessor(object):

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)  # turn-based
        actions = {
            'QUIT': False,
            'MOVE':{
                'mx': 0,
                'my': 0
            }
        }
        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        elif key.vk == libtcod.KEY_ESCAPE:
            actions['QUIT'] = True
            return actions  # exit game

        # movement keys
        if libtcod.console_is_key_pressed(libtcod.KEY_KP8) or libtcod.console_is_key_pressed(libtcod.KEY_UP):
            actions['MOVE']['my'] = -1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP2) or libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            actions['MOVE']['my'] = 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP4) or libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            actions['MOVE']['mx'] = -1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP6) or libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            actions['MOVE']['mx'] = 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
            actions['MOVE']['mx'] = -1
            actions['MOVE']['my'] = -1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
            actions['MOVE']['mx'] = 1
            actions['MOVE']['my'] = -1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
            actions['MOVE']['mx'] = -1
            actions['MOVE']['my'] = 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
            actions['MOVE']['mx'] = 1
            actions['MOVE']['my'] = 1

        return actions
