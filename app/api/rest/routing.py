"""
REST API Resource Routing

http://flask-restful.readthedocs.io/en/latest/
"""
from flask import request
from random import randint
from app.api.rest.base import BaseResource, SecureResource, rest_resource
from config import REDIS_URL, REDIS_CHAN_CURR, REDIS_CHAN_GRAPH, REDIS_CHAN_LIST, CURR_CODES

import redis,json,threading,requests

#from app.api.rest.listen import Listener

r = redis.from_url(REDIS_URL)
#client = Listener(r, [REDIS_CHAN_CURR])
#client.start()

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
    """ /api/currencies/list """
    endpoints = ['/currencies/list']

    def get(self):
        """
        temp = r.get(REDIS_CHAN_CURR)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        # Prepare data.
        my_json = temp.decode('utf8')
        data = eval(my_json)
        """
        return { 'currencies': CURR_CODES }

@rest_resource
class ResourceTwo(BaseResource):
    """ api/currencies/latest/graph """
    endpoints = ['/currencies/latest/graph']

    def get(self):
        temp = r.get(REDIS_CHAN_GRAPH)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        # Prepare data. Adapted from: https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format
        my_json = temp.decode('utf8')
        data = json.loads(my_json)
        # defaults to 200
        return data

@rest_resource
class ResourceThree(BaseResource):
    """ /api/currencies/latest/graph """
    endpoints = ['/currencies/latest/graph/<string:curr_one>/<string:curr_two>']

    def get(self, curr_one, curr_two):
        temp = r.get(REDIS_CHAN_GRAPH)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        my_json = temp.decode('utf8')
        data = json.loads(my_json)
        # https://medium.com/@happymishra66/lambda-map-and-filter-in-python-4935f248593
        data['datasets'] = list(filter(lambda x : x['label'] == curr_one or x['label'] == curr_two, data['datasets']))
        return data

@rest_resource
class ResourceFour(BaseResource):
    """ api/currencies/latest/list """
    endpoints = ['/currencies/latest/list']

    def get(self):
        temp = r.get(REDIS_CHAN_LIST)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        my_json = temp.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        return data