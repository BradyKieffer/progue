""" A general AI for each actor to implement """
from collections import defaultdict
from progue.ai.actions.action_stack import ActionStack

class AI(object):

    def __init__(self, actor, bored, brain=None):
        self.actor = actor
        self.bored = bored

        self.action_stack = ActionStack(self.actor)
        self.attributes = defaultdict(float)

        self.brain = brain

    def on_update(self):
        if self.action_stack.empty():
            self.spawn_action()

        self.action_stack.on_update()

    def check_for_action(self):
        """ Meant to be overridden, by default will return bored """
        action = self.bored
        if self.brain is not None:
            for fltr in self.brain:
                action = fltr(self.actor).filter_action(action)

        return action
    
    def new_action(self, action):
        """ Directly feed a new action to the stack useful when actions spawn more actions """
        self.action_stack.add_action_direct(action)

    def spawn_action(self):
        label = self.check_for_action()
        self.action_stack.add_action(label)