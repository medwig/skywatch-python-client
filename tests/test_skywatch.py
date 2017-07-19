#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from skywatch.cli import main
from skywatch import client 


#def test_cli_main():
#    main([])


class Test_Client(unittest.TestCase):
    """Tests for `Client` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_init(self):
        """Test init for client instance."""
        assert client.Client() is not None

