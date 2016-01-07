from language.processors import Similarities
from manager import mongo_connection_record
from nltk.corpus import stopwords
from collections import defaultdict
import unittest
import os


@unittest.skipIf(os.environ.get('TRAVIS', None) is not None, "Skipping in Travis CI builds")
class TestSimilarities(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stpwrds = stopwords
        self._mcr = mongo_connection_record
        self._transformer = None

    def setUp(self):
        if self._transformer is None:
            self._transformer = Similarities(self._mcr, self._stpwrds.words('english'))

    def test_similarity_threshold(self):
        threshold = self._transformer.similarity_threshold
        self.assertIsInstance(threshold, float, "Is returned type a float?")
        self.assertGreaterEqual(threshold, 0, "Is return value >=0?")
        self.assertLessEqual(threshold, 1.0, "Is return value <=1?")

    def test_lsi_index_mapping(self):
        self.assertIsInstance(self._transformer.lsi_index_mapping, dict, "Is return type a dict?")

    def test_calculate_similarities(self):
        import numpy
        sims = self._transformer.calculate_similarities()
        self.assertIsInstance(sims, defaultdict, "Is return type defaultdict?")
        self.assertTrue(
                all([isinstance(t, tuple) and isinstance(t[0], int) and isinstance(t[1], numpy.float32) for l in
                     sims.values()
                     for
                     t in l]),
                "Are values a list of tuples (int - LSI model index, numpy.float32 - sim threshold)?")
