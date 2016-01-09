from scrappers.plugins.bbc import BBC
from tests.framework import RSSTestCase
import unittest


class TestBBC(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return BBC

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()

