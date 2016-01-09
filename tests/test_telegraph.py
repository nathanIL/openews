from scrappers.plugins.telegraph import Telegraph
from tests.framework import RSSTestCase
import unittest


class TestAljazeera(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return Telegraph

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()

