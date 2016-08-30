""" A general AI for each actor to implement """
class AI(object):
    def __init__(self, actor):
        self.actor = actor
        self.actor.owner = self # Circular but this could be useful