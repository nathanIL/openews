from scrappers.plugins.cbsnews import CBSNews
from tests.framework import RSSTestCase
import unittest


class TestCBS(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return CBSNews

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()



