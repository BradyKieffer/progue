""" logging utils """
import logging
import inspect
from functools import wraps


HASHES = '#' * 10
FORMAT = '[%(asctime)s] %(code_point)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(name='game_logger')

def log_message(message):
    stack = inspect.stack()
    try:
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_func = stack[1][0].f_code.co_name
        code_point = the_class + '.' + the_func + ':'
    except KeyError:
        the_func = stack[1][0].f_code.co_name
        code_point = the_func + ':'

    
    _log_msg(code_point=code_point, message=message)

def log_endl():
    _log_msg(code_point='', message='')

def _log_msg(code_point, message):
    d = {'code_point': code_point}
    logger.warning(message, extra=d)

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            code_point = args[0].__class__.__name__ + '.' + func.__name__ + ':'
        except IndexError:
            code_point = func.__name__ + ':'

        log_endl()
        _log_msg(code_point=code_point, message='BEGIN')
        log_endl()
        func(*args, **kwargs)
        log_endl()
        _log_msg(code_point=code_point, message='END')
        log_endl()

    return wrapper
