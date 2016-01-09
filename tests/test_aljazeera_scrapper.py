from scrappers.plugins.aljazeera import ALJazeera
from tests.framework import RSSTestCase
import unittest


class TestAljazeera(unittest.TestCase, RSSTestCase):
    def scrapper_class(self):
        return ALJazeera

    def setUp(self):
        self._scrapper = self.create_scrapper_instance()

