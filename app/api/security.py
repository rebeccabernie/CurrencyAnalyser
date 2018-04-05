""" Method decorators """
from functools import wraps
from flask_restful import abort

def validate_args(func):
    """ Validate input comming in """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if True:
            print("aborting")
            print(args)
            print(kwargs)
            return abort(401)
        else:
            return func(*args, **kwargs)
    return wrapper
