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