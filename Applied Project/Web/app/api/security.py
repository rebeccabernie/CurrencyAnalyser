""" Method decorators """
from functools import wraps
from flask_restful import abort
from config import CURR_CODES

def validate_args(func):
    """ Validate input comming in """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (kwargs['curr_one'] in CURR_CODES) and (kwargs['curr_two'] in CURR_CODES):
            return func(*args, **kwargs)
        else:
            return { 'error': 'Invalid request' }, 400
    return wrapper
