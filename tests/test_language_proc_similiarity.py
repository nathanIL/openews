"""
A test place for language related code.

"""
from language.processors import Similarity
from nltk.corpus import reuters, stopwords
import unittest
import os


class TestSimiliarity(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._similarity_obj = Similarity(nltk_corpus=reuters, stopwords=stopwords.words('english'))

    def test_instance(self):
        self.assertIsInstance(self._similarity_obj, Similarity, "Is instance correct?")

    def test_tokenized_corpus_sentences(self):
        self.assertIsInstance(self._similarity_obj.tokenized_corpus_sentences, list,
                              "Is property returns a list instance?")
        self.assertIs(self._similarity_obj.tokenized_corpus_sentences,
                      self._similarity_obj.tokenized_corpus_sentences, "Are two different calls yields the same list?")
        for element in self._similarity_obj.tokenized_corpus_sentences:
            self.assertIsInstance(element, list, "Is each element is a list itself?")

    @unittest.skipIf(os.environ.get('TRAVIS', None) is not None, "Skipping in Travis CI builds")
    def test_dictionary(self):
        from gensim.corpora.dictionary import Dictionary
        self.assertIsInstance(self._similarity_obj.dictionary, Dictionary, "Is return type a Dictionary?")
        self.assertGreater(len(self._similarity_obj.dictionary.keys()), 0, "Do we have a populated Dictionary?")

    @unittest.skipIf(os.environ.get('TRAVIS', None) is not None, "Skipping in Travis CI builds")
    def test_trasform_to_tfidf_model(self):
        from gensim.models import TfidfModel
        self.assertIsInstance(self._similarity_obj.trasform_to_tfidf_model(), TfidfModel)
        self.assertIs(self._similarity_obj.trasform_to_tfidf_model(),
                      self._similarity_obj.trasform_to_tfidf_model(), "Are two different calls yields the same instance?")

    @unittest.skipIf(os.environ.get('TRAVIS', None) is not None, "Skipping in Travis CI builds")
    def test_sentence_to_bow(self):
        sentence = "Indian Prime Minister Narendra Modi has met his Pakistani counterpart Nawaz Sharif during a " \
                   "surprise visit to the Pakistani city of Lahore."
        self.assertIsInstance(self._similarity_obj.sentence_to_bow(sentence), list, "Is return type a list?")
        self.assertTrue(all([isinstance(e, tuple) for e in self._similarity_obj.sentence_to_bow(sentence)]),
                        "Are all elements in the list really tuples?")

    def test_tokenize_sentence(self):
        self.assertIsInstance(self._similarity_obj.tokenize_sentence("Surfing is awesome!!"), list,
                              "Is return type a list instance?")

    def test_stopwords(self):
        self.assertIsInstance(self._similarity_obj.stopwords, list, "Is return type a list instance?")
        self.assertTrue(all([isinstance(e, str) for e in self._similarity_obj.stopwords]),
                        "Are all elements in the list really words? (strings)")
