import requests
import json
from .exceptions import (InvalidAPIKey)
from . import auth
from . import models


# Todo
'''
SEARCH:
    search
AOI:
    list
    describe
    create
    delete
    update
    results
'''

class Client:
    """ Main client interface to skywatch API """

    default_aoi_config = models.Configuration.aoi_default

    def __init__(self, api_key=None, base_url=models.BASE_URL):
        """
        :param str api_key: API key to use. If None then checks ~/skywatch.json for api-key
        :param str base_url: The base URL to use. Optional, should not be needed.
        """
        try:
            self.api_key = api_key or auth.get_api_key()
            assert self.api_key is not None
        except (AssertionError, KeyError, IOError) as e:
            raise InvalidAPIKey(e)
        self.headers = {'x-api-key': self.api_key}


    def _call_api(self, method, url, params=None, body=None, headers=None):
        """ Executes the call to the api using the requests library """
        if headers:
            headers.update(self.headers)
        else:
            headers = self.headers

        print('Calling API with: method={method}, url={url}, headers={headers}, params={params}, body={body}'.format(**locals()))
        if method in ('PUT', 'POST'):
            response = requests.request(method, url, headers=headers, json=body)
        else:
            response = requests.request(method, url, headers=headers, params=params)

        print('Response from API: {}'.format(response.content))
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
        method = 'GET'
        body = None
        params = request

        if not isinstance(request, dict):
            raise TypeError('The search request parameters must be a dictionary, not {0}'.format(type(request)))

        location = request['location']
        if isinstance(location, list):
            request['location'] = self._polygon2str(location)

        url, _body = models.Request(endpoint, params=params, body=body).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def list_aois(self, aoi_id=None):
        """ Returns all aoi configurations associated with the user's api key.
        :param request: sky.list_aois()
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi'
        method = 'GET'
        body = None
        params = None

        url, body = models.Request(endpoint, params=params, body=body).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def describe_aoi(self, aoi_id):
        """ Returns the aoi configuration with the given aoi id. If no aoi id give then all aois configurations
        associated with the user's api key are returned.
        :param request: sky.describe_aoi(aoi_id=None)
        :example request: sky.describe_aoi('aoi-id-42')
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi'
        method = 'GET'
        body = None
        params = aoi_id

        url, body = models.Request(endpoint, params=params, body=body).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def create_aoi(self, configuration=None):
        """ Creates a new aoi configuration.
        :param request: sky.create_aoi(configuration={})
        :example request: sky.create_aoi(configuration={'location':[10,10,11,11], 'start_date': '2017-07-01'})
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi'
        method = 'POST'
        body = configuration
        params = None

        if not configuration or not isinstance(configuration, dict):
            raise TypeError('The aoi configuration must be a dict, not {0}'.format(type(configuration)))

        # /aoi requires aoi_location rather than location
        body['aoi_location'] = body.get('location') or body.get('aoi_location')
        if body.get('location'):
            del body['location']

        url, body = models.Request(endpoint, params=params, body=body).formatted()
        response = self._call_api(method, url, body=body)
        return models.Response(response).formatted()


    def list_aoi_results(self, aoi_id):
        """ Returns the pipeline results for the given aoi id.
        :param request: sky.list_aoi_results(aoi_id=None)
        :example request: sky.list_aoi_results('aoi-id-42')
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi/results'
        method = 'GET'
        params = aoi_id

        url, _body = models.Request(endpoint, params=params).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def delete_aoi(self, aoi_id):
        """ Deletes the pipeline with the aoi_id.
        :param request: sky.delete_aoi(aoi_id=None)
        :example request: sky.delete_aoi('aoi-id-42')
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi'
        method = 'DELETE'
        params = aoi_id

        url, _body = models.Request(endpoint, params=params).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def update_aoi(self, aoi_id, configuration):
        """ Updates the pipeline definition with the aoi_id.
        :param request: sky.update_aoi(aoi_id=None, configuration={})
        :example request: sky.update_aoi(aoi_id='aoi-id-42', configuration={'frequency': 'weekly', 'resolution': 10})
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/aoi'
        method = 'PUT'
        params = aoi_id

        url, body = models.Request(endpoint, params=params, body=configuration).formatted()
        response = self._call_api(method, url, body=body)
        return models.Response(response).formatted()


    def list_algorithms(self):
        """ show all algorithms that can be added to a pipeline
        :param request: sky.list_algorithms()
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/ai'
        method = 'GET'
        params = None

        url, _body = models.Request(endpoint, params=params).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()


    def describe_algorithm(self, ai_id):
        """ Returns the algorithm configuration with the given ai id
        :param request: sky.describe_agorithm(ai_id=None)
        :example request: sky.describe_algorithm('ai-id-42')
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error
        """
        endpoint = '/ai'
        method = 'GET'
        body = None
        params = ai_id

        url, _body = models.Request(endpoint, params=params).formatted()
        response = self._call_api(method, url)
        return models.Response(response).formatted()

