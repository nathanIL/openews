from scrappers.plugins.reuters import Reuters
from unittest.mock import MagicMock
from tests.rss_utils import RSSTestCase
import unittest


class TestReuters(unittest.TestCase, RSSTestCase):
    def setUp(self):
        self._scrapper_class = Reuters
        self._scrapper = self._scrapper_class()
        self._fixture = 'reuters'
        self._data = self.mock_resource_urls()
        self._title_counts = tuple([10,15,30])

        self._scrapper.resource_urls = MagicMock(return_value=self._data)
