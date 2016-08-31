""" Action constants """

ACTION_NONE = 'None'
ACTION_WANDER = 'ActorWander'
ACTION_MOVE = 'ActorMove'
ACTION_IDLE = 'Idle'

ACTIONS = {}

def get_action(label):
    return ACTIONS[label]

from progue.ai.actions.movement import ActionMove, ActionWander
from progue.ai.actions.misc import ActionIdle

ACTIONS = {
    ACTION_WANDER: ActionWander,
    ACTION_MOVE: ActionMove,
    ACTION_IDLE: ActionIdle
}