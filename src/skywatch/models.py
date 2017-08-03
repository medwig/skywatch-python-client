import json
from .exceptions import (SkywatchException, InvalidRequestError)

BASE_URL = 'https://api.skywatch.co'

class Configuration:
    aoi_default = {
        'location': [
                [
                  -80.54248809814453,
                  43.448432557680064
                ],
                [
                  -80.49270629882812,
                  43.448432557680064
                ],
                [
                  -80.49270629882812,
                  43.47883342917123
                ],
                [
                  -80.54248809814453,
                  43.47883342917123
                ],
                [
                  -80.54248809814453,
                  43.448432557680064
                ]
              ],
        'time': '2017-01-01',
        'level': 1,
        'frequency': 'weekly',
        'resolution': 30,
        'cloudcover': 80,
        'ai_id': "154311a8-582a-11e7-b30d-7291b81e23e"
    }


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


    def _geojson2location(self, body):
        try:
            loc = body.get('aoi_location')
            location = loc['features'][0]['geometry']
            body['aoi_location'] = location
            return body
        except Exception as e:
            return body


    def formatted(self):
        """Formats a request to the the api"""
        if self.endpoint == '/aoi':
            pass

        url = BASE_URL + self.endpoint + '/'
        url += self._params2query(self.params)
        body = self._geojson2location(self.body)
        return url, body
