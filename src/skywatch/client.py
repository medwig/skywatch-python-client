import requests
from .exceptions import (InvalidAPIKey)
from . import auth
from . import models


class Client:
    """ Main client interface to skywatch API """

    def __init__(self, api_key=None, base_url=models.BASE_URL):
        """
        :param str api_key: API key to use. Defaults to environment variable.
        :param str base_url: The base URL to use. Optional, should not be needed.
        """
        try:
            self.api_key = api_key or auth.get_api_key()
        except Exception as e:
            raise InvalidAPIKey(e)
        self.headers = {'x-api-key': self.api_key}


    def _call_api(self, method, url, params=None, body=None, headers=None):
        """ Executes the call to the api using the requests library """
        if headers:
            headers.update(self.headers)
        else:
            headers = self.headers
        response = requests.request(method.upper(), url, headers=headers, params=params, data=body)
        return response.content


    def _polygon2str(self, polygon):
        """ Convertes a polygon list of lists to a flattened list """
        flatList = [value for point in polygon for value in point]
        return ','.join(map(str, flatList))


    def search(self, request):
        """ Searches the /data endpoint for satellite imagery
        :param request: sky.search({"location": "x1,y1,x2,y2..xn,yn", "time": "daterange", "addition_filters": "foo"})
        :example request: sky.search({"location": "10,10,11,11", "time": "2017-01-01", "cloudcover": "10"})
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/data'
        method = 'get'
        body = None
        params = request
        if not isinstance(request, dict):
            raise TypeError('The search request parameters must be a dictionary, not {0}'.format(type(request)))

        location = request['location']
        if isinstance(location, list):
            request['location'] = self._polygon2str(location)

        url = models.Request(endpoint, params=params, body=body).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def describe_aoi(self, aoi_id=None):
        """ Returns the aoi configuration with the given aoi id. If no aoi id give then all aois configurations
        associated with the user's api key are returned.
        :param request: sky.describe_aoi(aoi_id=None)
        :example request: sky.describe_aoi('aoi-id-42')
        :example request: sky.describe_aoi()
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi'
        method = 'get'
        body = None
        params = aoi_id

        url = models.Request(endpoint, params=params, body=body).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


