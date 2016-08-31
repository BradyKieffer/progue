""" Misc / Weird actions can go here """
import random
from action import Action
from progue.utils.actor_constants import ATTRIBUTE_IDLE, ATTR_VALUE, MAX_TURNS, CURRENT_TURN, RANGE


class ActionIdle(Action):
    """ Used for lazy monsters """

    def __init__(self, actor):
        Action.__init__(self, actor=actor, update_func=self.idle)

        self.actor.attributes[ATTRIBUTE_IDLE][ATTR_VALUE] = True
        rng = self.actor.attributes[ATTRIBUTE_IDLE][RANGE]
        self.percent_idle = max(min(rng[1], random.random()), rng[0])
        self.curr_turn = self.actor.attributes[ATTRIBUTE_IDLE][CURRENT_TURN]
        self.max_turns = self.actor.attributes[ATTRIBUTE_IDLE][
            MAX_TURNS] + random.randrange(-5, 5)

    def idle(self):
        if (self.curr_turn > self.max_turns) or (random.random() > self.percent_idle):
            self.complete = True
            self.actor.attributes[ATTRIBUTE_IDLE][ATTR_VALUE] = False

        self.curr_turn += 1
