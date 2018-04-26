""" API Backend - Base Resource Models """

#from flask_restful import Resource, abort
from flask_restplus import Resource, abort

from app.api import api_rest
from app.api.security import validate_args

class BaseResource(Resource):

    def get(self, *args, **kwargs):
        abort(405)

class SecureResource(BaseResource):
    method_decorators = [validate_args]

def rest_resource(resource_cls):
    """ Decorator for adding resources to Api App """
    api_rest.add_resource(resource_cls, *resource_cls.endpoints)
