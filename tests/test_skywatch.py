#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import pytest

from skywatch.cli import main
from skywatch import exceptions
from skywatch import auth
import skywatch

#def test_cli_main():
#    main([])

INVALID_API_KEY = 'fake-api-key'
VALID_API_KEY = auth.get_apikey_from_config()

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



class Test_Client(unittest.TestCase):
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

    def test_init_missing_apikey(self):
        """Passing an empty api-key raises exception - for now"""
        try:
            sky = skywatch.Client(api_key=None)
        except exceptions.InvalidAPIKey as e:
            assert str(e) == 'api_key is required'

    def test_get_api_key_from_config(self):
        """Failing to pass an api-key checks config file"""
        sky = skywatch.Client()
        assert sky


    # Test sky.search()
    def test_polygon2str(self):
        """Test conversion of a polygon into a flat string"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        result = sky._polygon2str([[1, 1], [2, 2]])
        assert result == '1,1,2,2'
     
#    @mock.patch('skywatch.client.Client._call_api', side_effect=mock__call_api)
#    def test_search(self, mock_request):
#        """Test that a search call handles input safely"""
#        sky = skywatch.Client(api_key=VALID_API_KEY)
#        request = {
#            'location': [[10, 10], [11, 11]],
#            'time': '2017-01' 
#        }
#        result = sky.search(request)
#        assert result == True
#



    # INTEGRATION TESTS

    def test_search_with_valid_request(self):
        """Test that a basic call returns list of results"""
        sky = skywatch.Client(api_key=VALID_API_KEY)
        request = {
            'location': [[10, 10], [11, 11]],
            'time': '2017-01' 
        }
        result = sky.search(request)
        assert isinstance(result, list)


