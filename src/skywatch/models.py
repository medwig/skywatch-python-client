import json


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


    def format(self):
        try:
            response = json.loads(self.response)
        except Exception as e:
            response = self.response
        print(response)
        return response

