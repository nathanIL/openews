from scrappers.plugins.reuters import Reuters
from tests.framework import RSSTestCase
import unittest


class TestReuters(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return Reuters

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()

