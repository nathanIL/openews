from scrappers.plugins.nytimes import NYTimes
from tests.framework import RSSTestCase
import unittest


class TestNYTimes(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return NYTimes

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()
