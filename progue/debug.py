""" Misc functions that can be used to debug crap """
import os 
from lib import libtcodpy as libtcod

def print_all_chars():
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/terminal8x8_aa_as.png')
    libtcod.console_set_custom_font(font_path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
    libtcod.console_init_root(25, 80, 'Printing all characters', False)

    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(0, libtcod.white)
        j = 0
        i = 1
        for x in xrange(700):
            libtcod.console_put_char(0, i, j, x)
            j += 1
            if j > 80:
                i += 2
                j = 0

        libtcod.console_put_char(0, i + 2, 1, 177)
        libtcod.console_flush()

if __name__ == '__main__':
    print_all_chars()
    