from progue.utils.data_structures import Stack
from progue.utils.action_utils import get_action

class ActionStack(object):

    def __init__(self, actor):
        self.stack = Stack()
        self.actor = actor

    def add_action(self, label):
        action = get_action(label)(self.actor)
        self.stack.push(action)

    def add_action_direct(self, action):
        self.stack.push(action)

    def add_actions(self, actions):
        for label in actions:
            self.add_action(label)

    def empty(self):
        return self.stack.empty()

    def on_update(self):
        self.check_action()
        if not self.stack.empty():
            self.stack.peek().on_update()
        else:
            self.actor.ai.spawn_action()
        self.check_action()

    def check_action(self):
        action = self.stack.peek()
        if action.complete:
            self.stack.pop()

        elif action.failed:
            self.on_failed_action(action)

    def on_failed_action(self, action):
        if action.has_original_intent():
            original_intent = action.original_intent
            while not self.stack.peek() == original_intent:
                self.stack.pop()  # Fail back to the original intent

        else:
            self.stack.purge()
