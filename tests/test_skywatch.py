#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import pytest
import json

from skywatch.cli import main
from skywatch import exceptions
from skywatch import auth
from skywatch import models
import skywatch

#def test_cli_main():
#    main([])

INVALID_API_KEY = 'fake-api-key'
try:
    VALID_API_KEY = auth.get_api_key()
except:
    VALID_API_KEY = 'no-valid-api-key-found'

FULL_GEOJSON = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
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
          ]
        ]
      }
    }
  ]
}

GEOJSON = {
  "type": "Polygon",
  "coordinates": [
    [
      [15.4, 13.4],
      [15.8, 13.4],
      [15.8, 13.8],
      [15.4, 13.8],
      [15.4, 13.4]
    ]
  ]
}

AOI_DEFINITION = {
    'ai_id': "154311a8-582a-11e7-b30d-7291b81e23e",
    'frequency': 'weekly',
    'location': FULL_GEOJSON,
    'frequency': 'weekly',
    'start_date': '2017-07-11',
    'resolution': 10
}


# Mocks
def mock__call_api(*args, **kwargs):
    return True

def mock__returns_none(*args, **kwargs):
    return None



class Test_Auth(unittest.TestCase):
    """Tests for `Auth` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

#    def test_auth__read_config_file(self):
#        """Test json file is read"""
#        assert auth._read_config_file() is not None
#
#    def test_get_api_key(self):
#        """Test that api-key is loaded from config file"""
#        assert auth.get_api_key() is not None


class Test_Models(unittest.TestCase):
    """Tests for `Models` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_models_response(self):
        """Test that a response is returned from format_response"""
        resp = 'test response msg'
        assert models.Response(resp).formatted() is not None

    def test_models_response_format_with_json(self):
        """Test that a json is returned as an object by response"""
        response = json.dumps({'body': 'json test body'})
        assert isinstance(models.Response(response).formatted(), dict)

    def test_models_response_format_with_string(self):
        """Test that a non-json string is returned as string response"""
        response = 'string test body'
        assert isinstance(models.Response(response).formatted(), str)

    def test_models_request_format_with_string(self):
        """Test that a call to the /data request formatter returns as expected"""
        endpoint = '/data'
        params = {'test_param': 'foo'}
        body = None
        expected = 'https://api.skywatch.co/data/test_param/foo/'
        url, body = models.Request(endpoint=endpoint, params=params, body=body).formatted()
        assert (url, body) == (expected, None)


class Test_Client_search(unittest.TestCase):
    """Tests for `Client` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    # Test init of client instance
    def test_init_with_apikey(self):
        """Test that client instance contains passed api-key"""
        sky = skywatch.Client(api_key=INVALID_API_KEY)
        assert sky.api_key == INVALID_API_KEY

    @mock.patch('skywatch.auth.get_api_key', side_effect=mock__returns_none)
    def test_init_apikey_isNone(self, mock_request):
        """Passing an empty api-key with no config key present raises exception"""
        with pytest.raises(exceptions.InvalidAPIKey):
            print(skywatch.Client(api_key=None))

    # Test sky.search()
    def test_polygon2str(self):
        """Test conversion of a polygon into a flat string"""
        sky = skywatch.Client(api_key=INVALID_API_KEY)
        result = sky._polygon2str([[1, 1], [2, 2]])
        assert result == '1,1,2,2'

    @mock.patch('skywatch.client.Client._call_api', side_effect=mock__call_api)
    def test_search(self, mock_request):
        """Test that a search call handles required params"""
        sky = skywatch.Client(api_key=INVALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '2017-01'
        }
        result = sky.search(request)
        assert result == True

    @mock.patch('skywatch.client.Client._call_api', side_effect=mock__call_api)
    def test_search(self, mock_request):
        """Test that a search handles additional call params"""
        sky = skywatch.Client(api_key=INVALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '2017-01',
            'resolution': 10
        }
        result = sky.search(request)
        assert result == True


    # Test sky.describe_aoi
    def test_describe_aoi_fails_given_no_argument(self):
        """Test that describe_aoi without aoi_id raises a TypeError"""
        sky = skywatch.Client(api_key=INVALID_API_KEY)
        with pytest.raises(TypeError):
            sky.describe_aoi()

   # Test sky.describe_aoi
    def test_list_aoi_results_fails_given_no_argument(self):
        """Test that list_aoi_results without aoi_id raises a TypeError"""
        sky = skywatch.Client(api_key=INVALID_API_KEY)
        with pytest.raises(TypeError):
            sky.list_aoi_results()


#class Integration_Tests(unittest.TestCase):
#
#    def setUp(self):
#        """Set up test fixtures, if any."""
#
#    def tearDown(self):
#        """Tear down test fixtures, if any."""
#
#
#    def test_init_without_apikey(self):
#        """Tests that missing api-key is read from config file"""
#        sky = skywatch.Client()
#        assert sky.headers['x-api-key'] is not None
#
#
#    def test_search_with_missing_params(self):
#        """Test a search call lacking time or location returns error message"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        request = {
#            'location': [[10, 10], [11, 11]]
#        }
#        result = sky.search(request)
#        assert not isinstance(result, list)
#
#    def test_search_with_valid_request(self):
#       """Test that a basic call returns list of results"""
#       sky = skywatch.Client(api_key=VALID_API_KEY)
#       request = {
#           'location': [[10, 10], [11, 11]],
#           'time': '2017-01'
#       }
#       result = sky.search(request)
#       assert isinstance(result, list)
#
#    def test_search_returns_empty_list(self):
#        """Test that a search outside of available data returns an empty list object"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        request = {
#            'location': [[10, 10], [11, 11]],
#            'time': '1914-06-28'
#        }
#        result = sky.search(request)
#        assert result == []
#
#    def test_list_aois(self):
#        """Test that list_aoi returns a list"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        aois = sky.list_aois()
#        assert isinstance(aois, list)
#
#    def test_aoi_create_with_geojson(self):
#        """Test that creating an aoi returns a dict with aoi_id"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        new_aoi = sky.create_aoi(AOI_DEFINITION)
#        print(new_aoi)
#        new_aoi_id = new_aoi['id']
#        assert new_aoi_id and isinstance(new_aoi, dict)
#
#    def test_aoi_create_with_polygon(self):
#        """Test that creating an aoi returns a dict with aoi_id"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        aoi_def = AOI_DEFINITION.copy()
#        aoi_def['location'] = GEOJSON
#        new_aoi = sky.create_aoi(aoi_def)
#        print(new_aoi)
#        new_aoi_id = new_aoi['id']
#        assert new_aoi_id and isinstance(new_aoi, dict)
#
#    def test_aoi_delete(self):
#        """Test that deleting an aoi returns a dict with aoi_id"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        new_aoi = sky.create_aoi(AOI_DEFINITION)
#        new_aoi_id = new_aoi['id']
#        resp = sky.delete_aoi(new_aoi_id)
#        print(resp)
#        assert resp['delete'] == True
#
#    def test_aoi_delete(self):
#        """Test that trying to delete a non-existant aoi returns an error string"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        new_aoi = sky.create_aoi(AOI_DEFINITION)
#        resp = sky.delete_aoi('fake-aoi-id')
#        print(resp)
#        assert resp == 'AOI id does not exist'
#
#    def test_update_aoi_results(self):
#        """Test that update_aoi returns a dict"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        aoi_id = sky.list_aois()[0]['id']
#        resp = sky.update_aoi(aoi_id=aoi_id, configuration={'resolution': 10})
#        print(resp)
#        assert resp['resolution'] == 10
#
#    def test_list_algorithms(self):
#        """Test that list_algorithms returns a list"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        ais = sky.list_algorithms()
#        assert isinstance(ais, list)
#
#    def test_describe_algorithm(self):
#        """Test that describe_algorithm returns a dict"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        id = sky.list_algorithms()[0]['id']
#        ai = sky.describe_algorithm(id)
#        print(ai)
#        assert isinstance(ai, dict) and ai['id']
#
#
