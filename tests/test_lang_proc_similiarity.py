"""
A test place for language related code.
"""
from language.processors import Similarity
from nltk.corpus import reuters, stopwords
import unittest


class TestSimiliarity(unittest.TestCase):
    def setUp(self):
        self._similarity_obj = Similarity(nltk_corpus=reuters, stopwords=stopwords.words('english'))

    def test_instance(self):
        self.assertIsInstance(self._similarity_obj, Similarity, "Is instance correct?")

