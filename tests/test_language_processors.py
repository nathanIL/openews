from language.processors import Transformer
from manager import mongo_connection_record
from nltk.corpus import stopwords
import unittest
import os


@unittest.skipIf(os.environ.get('TRAVIS', None) is not None, "Skipping in Travis CI builds")
class TestTransformer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stpwrds = stopwords
        self._mcr = mongo_connection_record

    def setUp(self):
        self._transformer = Transformer(self._mcr, self._stpwrds.words('english'))

    def test_stopwords(self):
        self.assertIsInstance(self._transformer.stopwords, list, "Are stopwords returned as a list?")

    def test_similarity_threshold(self):
        threshold = self._transformer.similarity_threshold
        self.assertIsInstance(threshold, float, "Is returned type a float?")
        self.assertGreaterEqual(threshold, 0, "Is return value >=0?")
        self.assertLessEqual(threshold, 1.0, "Is return value <=1?")

    def test_calculate_similarities(self):
        self._transformer.calculate_similarities()
