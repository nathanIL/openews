from scrappers.plugins.foxnews import FoxNews
from tests.framework import RSSTestCase
import unittest


class TestFoxNews(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return FoxNews

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()


