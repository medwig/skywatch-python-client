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
VALID_API_KEY = auth.get_api_key()

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


# Mocks
def mock__call_api(*args, **kwargs):
    return True


class Test_Auth(unittest.TestCase):
    """Tests for `Auth` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_auth__read_config_file(self):
        """Test json file is read"""
        assert auth._read_config_file() is not None

    def test_get_api_key(self):
        """Test that api-key is loaded from config file"""
        assert auth.get_api_key() is not None


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
        req = models.Request(endpoint=endpoint, params=params, body=body)
        assert req.formatted() == expected


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

    def test_init_apikey_isNone(self):
        """Passing an empty api-key raises exception - for now"""
        try:
            sky = skywatch.Client(api_key=None)
        except exceptions.InvalidAPIKey as e:
            assert str(e) == 'api_key is required'

    def test_init_without_apikey(self):
        """Tests that missing api-key is read from config file"""
        sky = skywatch.Client()
        assert sky.headers['x-api-key'] is not None


    # Test sky.search()
    def test_polygon2str(self):
        """Test conversion of a polygon into a flat string"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        result = sky._polygon2str([[1, 1], [2, 2]])
        assert result == '1,1,2,2'

    @mock.patch('skywatch.client.Client._call_api', side_effect=mock__call_api)
    def test_search(self, mock_request):
        """Test that a search call handles required params"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '2017-01'
        }
        result = sky.search(request)
        assert result == True

    @mock.patch('skywatch.client.Client._call_api', side_effect=mock__call_api)
    def test_search(self, mock_request):
        """Test that a search handles additional call params"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '2017-01',
            'resolution': 10
        }
        result = sky.search(request)
        assert result == True


class Integration_Tests(unittest.TestCase):
    """Tests for `Auth` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_search_with_missing_params(self):
        """Test a search call lacking time or location returns error message"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]]
        }
        result = sky.search(request)
        assert not isinstance(result, list)


    def test_search_with_valid_request(self):
        """Test that a basic call returns list of results"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '2017-01'
        }
        result = sky.search(request)
        assert isinstance(result, list)

    def test_search_returns_empty_list(self):
        """Test that a search outside of available data returns an empty list object"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '1914-06-28'
        }
        result = sky.search(request)
        assert result == []

    def test_aoi_describe_all(self):
        """Test that an aoi config request without aoi_id returns a list"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        all_aois = sky.describe_aoi()
        assert isinstance(all_aois, list)

    def test_aoi_describe_aoi(self):
        """Test that an aoi config request with aoi_id returns a dict"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        all_aois = sky.describe_aoi()
        assert isinstance(all_aois[0], dict)

    def test_aoi_create(self):
        """Test that creating an aoi returns a dict"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        new_aoi = sky.create_aoi()
        assert isinstance(new_aoi, dict)
