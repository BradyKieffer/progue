""" Actor maps """
from progue.lib import libtcodpy as libtcod 
from progue.utils   .actor_constants import *
from progue.actors.jackal import JackalAI, Jackal
from progue.actors.player import Player


# Every actor attribute will be in this dict
ACTOR_ATTRIBUTES = {
    PLAYER: {
        NAME: PLAYER,
        CLASS:      Player,
        AI:         None,
        GLYPH:      '@',
        FORE_COLOR: libtcod.white, 
        BACK_COLOR: libtcod.black,
        
        ATTRIBUTES: {
            ATTRIBUTE_HEALTH: 100.0
        }
    },
    ACTOR_JACKAL: {
        NAME: ACTOR_JACKAL,
        CLASS:      Jackal,
        AI:         JackalAI,
        GLYPH:      'j',
        FORE_COLOR: libtcod.sepia, 
        BACK_COLOR: libtcod.black,
        
        ATTRIBUTES: {
            ATTRIBUTE_HEALTH: 25.0,
            ATTRIBUTE_IDLE: {
                ATTR_VALUE:   False,
                CURRENT_TURN: 0, 
                MAX_TURNS:    10,
                RANGE:        (0.2, 0.6)
            }
        }
    }
}

def get_actor(label):
    return ACTOR_ATTRIBUTES[label]