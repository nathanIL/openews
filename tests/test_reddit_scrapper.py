from scrappers.plugins.reddit import Reddit
from tests.framework import RSSTestCase
import unittest


class TestReddit(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return Reddit

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()


