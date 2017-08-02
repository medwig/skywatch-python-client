import json
from .exceptions import (SkywatchException, InvalidRequestError)

BASE_URL = 'https://api.skywatch.co'


class Data:
    request = [
        'location',
        'time',
        'level',
        'resolution',
        'cloudcover',
        'band',
        'source',
        'limit',
        'clipping'
    ]

    response = {}


class Response:
    """Formats an api response for the client."""

    def __init__(self, response):
        self.response = response

    def formatted(self):
        try:
            #response = self.response.encode('utf-8')
            response = json.loads(self.response)
        except (TypeError, ValueError):
            response = self.response
        return response


class Request:
    """Formats an api request, returns a formatted url and body"""

    def __init__(self, endpoint, params=None, body=None):
        self.endpoint = endpoint
        self.body = body
        self.params = params

    def _params2query(self, params):
        if not params:
            return ''
        try:
            paramString = ''.join(['{}/{}/'.format(k, v) for k, v in params.items()])
        except AttributeError:
            paramString = str(params)

        return paramString

    def formatted(self):
        """Formats a request to the the api"""
        if self.endpoint == '/aoi':
            pass

        url = BASE_URL + self.endpoint + '/'
        url += self._params2query(self.params)
        body = self.body
        return url, body
