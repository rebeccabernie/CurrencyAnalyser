"""
REST API Resource Routing

http://flask-restful.readthedocs.io/en/latest/
"""
from flask import request
from app.api import api_rest
from flask_restplus import Resource, abort, fields
from app.api.rest.base import BaseResource, rest_resource
from config import REDIS_URL, REDIS_CHAN_GRAPH, REDIS_CHAN_LIST, CURR_CODES, REDIS_CHAN_ML_BTC_GRAPH, REDIS_CHAN_ML_BTC

import redis,json,threading,requests

r = redis.from_url(REDIS_URL)

pred = api_rest.model('Prediction', {
    'prediction': fields.String(description='prediction'),
})
cdataset = api_rest.model('CurrencyData', {
    'label': fields.String(description='currency'),
    'backgroundColor': fields.String(description='color'),
    'data': fields.List(fields.String, description='prices')
})
cgraph = api_rest.model('CurrencyGraph', {
    'labels': fields.List(fields.String, description='dates'),
    'datasets': fields.List(fields.Nested(cdataset))
})
currency = api_rest.model('Currency', {
    'code': fields.String(description='currencycode'),
    'name': fields.String(description='currency'),
    'symbol': fields.String(description='symbol'),
    'data': fields.String(description='rate')
})
clist = api_rest.model('CurrencyList', {
    'currencies': fields.List(fields.String, description='currencies')
})
clatestlist = api_rest.model('CurrencyLastestList', {
    'currencies': fields.List(fields.Nested(currency), description='currencies')
})
error = api_rest.model('Error', {
    'error': fields.String(description='error'),
})

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
    endpoints = ['/list']

    @api_rest.doc('get_currencies')
    @api_rest.response(404, 'Not Found', error)
    @api_rest.response(200, 'Success', clist)
    def get(self):
        return { 'currencies': CURR_CODES }

@rest_resource
class ResourceTwo(BaseResource):
    """ api/currencies/latest/graph """
    endpoints = ['/latest/graph']

    @api_rest.doc('get_latest_graph')
    @api_rest.response(404, 'Not Found', error)
    @api_rest.response(200, 'Success', cgraph)
    def get(self):
        temp = r.get(REDIS_CHAN_GRAPH)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        # Prepare data. Adapted from: https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format
        my_json = temp.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        # defaults to 200
        return data

@rest_resource
class ResourceThree(BaseResource):
    """ /api/currencies/latest/graph """
    endpoints = ['/latest/graph/<string:curr_one>/<string:curr_two>']

    @api_rest.doc('get_latest_graph_two')
    @api_rest.response(404, 'Not Found', error)
    @api_rest.response(200, 'Success', cgraph)
    def get(self, curr_one, curr_two):
        temp = r.get(REDIS_CHAN_GRAPH)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        my_json = temp.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        # https://medium.com/@happymishra66/lambda-map-and-filter-in-python-4935f248593
        data['datasets'] = list(filter(lambda x : x['label'] == curr_one or x['label'] == curr_two, data['datasets']))
        return data

@rest_resource
class ResourceFour(BaseResource):
    """ api/currencies/latest/list """
    endpoints = ['/latest/list']

    @api_rest.doc('get_latest_currencies')
    @api_rest.response(404, 'Not Found', error)
    @api_rest.response(200, 'Success', clatestlist)
    def get(self):
        temp = r.get(REDIS_CHAN_LIST)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        my_json = temp.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        return data

@rest_resource
class ResourceFive(BaseResource):
    """ api/ml/btc/graph """
    endpoints = ['/ml/btc/graph']

    @api_rest.doc('get_ml_btc_graph')
    @api_rest.response(404, 'Not Found', error)
    @api_rest.response(200, 'Success', cgraph)
    def get(self):
        temp = r.get(REDIS_CHAN_ML_BTC_GRAPH)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        my_json = temp.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        return data

@rest_resource
class ResourceSix(BaseResource):
    """ api/ml/btc """
    endpoints = ['/ml/btc']

    @api_rest.doc('get_ml_btc')
    @api_rest.response(404, 'Not Found', error)
    @api_rest.response(200, 'Success', pred)
    def get(self):
        temp = r.get(REDIS_CHAN_ML_BTC)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        data = temp.decode('utf8')
        return {'prediction': data }