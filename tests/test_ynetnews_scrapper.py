from scrappers.plugins.ynetnews import YnetNews
from unittest.mock import MagicMock
from tests.framework import RSSTestCase
import unittest


class TestYnetNews(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return YnetNews

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()
        self._fixture = 'ynetnews'
        self._data = self.mock_resource_urls()
        self._title_counts = tuple([5, 10, 13])

        self._scrapper.resource_urls = MagicMock(return_value=self._data)
