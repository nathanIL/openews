from scrappers.plugins.bbc import BBC
from unittest.mock import MagicMock
from tests.framework import RSSTestCase
import unittest


class TestBBC(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return BBC

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()
        self._fixture = 'bbc'
        self._data = self.mock_resource_urls()
        self._title_counts = tuple([10, 15])

        self._scrapper.resource_urls = MagicMock(return_value=self._data)

