"""
REST API Resource Routing

http://flask-restful.readthedocs.io/en/latest/
"""

import time
from flask import request
from app.api.rest.base import BaseResource, SecureResource, rest_resource

""" 
TODO: stream route here 
ref: https://stephennewey.com/realtime-websites-with-flask/
"""

"""
Why Server-Sent Event(SEE) Stream?
Websockets(WSs) are often favoured over SEEs as they provide a protocol surpassing that of SEEs. 
WSs provide bi-directional, full-duplex communication between the server and client.
However, this is only significant when two way communication is required.
For data that does not need to be sent from the client, traditional HTTP SEEs, that do not implement full-duplex communication and the subsequent new WS servers to handle this connection, are ideal.
Also, SSEs have a number of functionalities that WSs lack, such as automatic reconnection.
ref: https://www.html5rocks.com/en/tutorials/eventsource/basics/
"""
@rest_resource
class ResourceOne(BaseResource):
    """ /api/resource/one """
    endpoints = ['/resource/one']

    def get(self):
        time.sleep(1)
        return {'name': 'Resource One', 'data': True}

    def post(self):
        json_payload = request.json
        return {'name': 'Resource Post'}


@rest_resource
class SecureResourceOne(SecureResource):
    """ /api/resource/two """
    endpoints = ['/resource/two/<string:resource_id>']

    def get(self, resource_id):
        time.sleep(1)
        return {'name': 'Resource Two', 'data': resource_id}

