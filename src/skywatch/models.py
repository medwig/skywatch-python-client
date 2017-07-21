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
            response = json.loads(self.response)
        except Exception as e:
            response = self.response
        print(response)
        return response


class Request:
    """Formats an api request, returns a formatted url and body"""

    def __init__(self, endpoint, params=None, body=None):
        self.endpoint = endpoint
        self.body = body
        self.params = params

    def _params2query(self, params):
        if params:
            paramString = ''.join(['{}/{}/'.format(k, v) for k, v in params.items()])
        else:
            paramString = ''
        return paramString


    def formatted(self):
        """Formats a request to the the api"""
        url = BASE_URL + self.endpoint + '/'
        url += self._params2query(self.params)
        return url
