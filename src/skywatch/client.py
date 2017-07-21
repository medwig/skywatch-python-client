import requests
from .exceptions import (InvalidAPIKey)
from . import auth

BASE_URL = 'https://api.skywatch.co/'


class Client:
    """ Main client interface to skywatch API """    

    def __init__(self, api_key=None, base_url=BASE_URL):
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
        print(method, url, headers)
        response = requests.request(method.upper(), url, headers=headers, params=params, data=body)
        return response


    def _polygon2str(self, polygon):
        """ Convertes a polygon list of lists to a flattened list """
        flatList = [value for point in polygon for value in point]
        return ','.join(map(str, flatList))
        

    def search(self, request):
        """ Searches the data endpoint
        :param request: see :ref:`api-search-request`
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error.
        """
        if not isinstance(request, dict):
            raise TypeError('The search request parameters must be a dictionary, not {0}'.format(type(request)))

        location = request['location']
        if isinstance(location, list):
            request['location'] = self._polygon2str(location)

        url = BASE_URL + 'data/'
        url += '/'.join([k + '/' + v for k, v in request.items()])
        response = self._call_api('get', url)
        return response.json()

