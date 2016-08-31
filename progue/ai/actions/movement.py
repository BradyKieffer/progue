""" Movement related actions stored here """
import random
from action import Action
from progue.utils.action_utils import get_action, ACTION_MOVE

class ActionMove(Action):
    """ Move the actor in the direction provided """
    def __init__(self, mx, my, actor):
        Action.__init__(self, actor=actor, update_func=self.move)
        self.mx = mx
        self.my = my

    def move(self):
        if self.actor.move_to(mx=self.mx, my=self.my):
            self.complete = True
        else:
            self.failed = True

class ActionWander(Action):

    def __init__(self, actor):
        Action.__init__(self, actor=actor, update_func=self.wander)

    def wander(self):
        if not self.check_complete():
            # Computes a random movement direction and returns it
            mx = my = 0
            (prob_x, prob_y) = (random.random(), random.random())
            
            if prob_x > 0.5:
                mx = 1
            else:
                mx = -1

            if prob_y > 0.5:
                my = 1
            else:
                my = -1

            self.action_move = get_action(ACTION_MOVE)(mx=mx, my=my, actor=self.actor)
            self.actor.ai.new_action(self.action_move)

    def check_complete(self):
        if hasattr(self, 'action_move'):
            self.complete = self.action_move.complete
            self.failed = self.action_move.failed

        return self.complete or self.failed