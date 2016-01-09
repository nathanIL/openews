from scrappers.plugins.ynetnews import YnetNews
from tests.framework import RSSTestCase
import unittest


class TestYnetNews(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return YnetNews

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()

