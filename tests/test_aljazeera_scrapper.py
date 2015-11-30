# from nose.tools import nottest, with_setup, assert_is_instance, assert_equal, assert_true
# from scrappers.plugins.aljazeera import ALJazeera
# import os
# import validators
from scrappers.plugins.aljazeera import ALJazeera
from unittest.mock import MagicMock
from tests.rss_utils import RSSTestCase
import unittest


class TestAljazeera(unittest.TestCase, RSSTestCase):
    def setUp(self):
        self._scrapper_class = ALJazeera
        self._scrapper = self._scrapper_class()
        self._fixture = 'aljazeera'
        self._data = self.mock_resource_urls()
        self._title_counts = tuple([10,15])

        self._scrapper.resource_urls = MagicMock(return_value=self._data)
