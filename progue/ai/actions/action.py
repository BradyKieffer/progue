""" The idea of using a stack to store actions was gathered from: https://www.youtube.com/watch?v=4uxN5GqXcaA """
class Action(object):

    def __init__(self, actor, update_func, original_intent=None):
        self.complete = self.failed = False
        self.update_func = update_func
        self.actor = actor
        self.original_intent = original_intent

    def on_update(self):
        self.update_func()

    def has_original_intent(self):
        return self.original_intent is not None