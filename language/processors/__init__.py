from nltk.tokenize import word_tokenize
from server.db import MongoClientContext
from operator import itemgetter
from server import server_app
from collections import defaultdict
from itertools import chain
import string
import tempfile
import os
import nltk
import logging

nltk.data.path.append('nltk_data')


class Similarities(object):
    """
    Class for text similarities stuff
    """

    def __init__(self, mongo_client_ctx, stopwords):
        self._stopwords = stopwords
        self._mongo_client_ctx = mongo_client_ctx
        self._lsi_mapping = dict()
        self._sim_index = None
        self._dictionary = None
        self._lsimodel = None

        self._run_transformers()

    @staticmethod
    def logger():
        """
        Scrapper's specific logger instance. Use this to log inside scrappers.
        :return: Returns a logging.Logger('openews.scrappers') instance.
        """
        return logging.getLogger('openews.language')

    @property
    def considerable_doc_property(self):
        """
        The document property to use for training. this is the actually data we take from the MongoDB documents to
        parse and train.
        :return: str
        """
        return 'title'

    @property
    def dictionary_file(self):
        """
        The filename to use when serializing gensim.corpora.dictionary.Dictionary to disk.
        :return: str
        """
        return "openews.processors.dict"

    @property
    def dictionary(self):
        """
        The used Dictionary.
        :return: gensim.corpora.dictionary.Dictionary
        """
        return self._dictionary

    @property
    def lsi_model(self):
        """
        The used LSI model.
        :return: gensim.models.lsimodel.LsiModel
        """
        return self._lsimodel

    @property
    def similarity_index(self):
        """
        The similarity index instance
        :return: gensim.similarities.docsim.MatrixSimilarity
        """
        return self._sim_index

    @property
    def similarity_threshold(self):
        """
        The similarity threshold.
        Anything above or equals to this value will be considered as similar document.
        :return: float
        """
        return server_app.config['SIMILARITY_THRESHOLD']

    @property
    def lsi_index_mapping(self):
        """
        A mapping between the LSI model index (key) and the documents (Collection the document is in, document)
        :return: dict
        """
        return self._lsi_mapping

    @staticmethod
    def _create_resource_path(resource_file):
        """
        Creates a absolute path to resource_file based on the given system's temp directory.
        :param resource_file: str
        :return: str
        """
        return os.path.join(tempfile.gettempdir(), resource_file)

    def _resource_exists(self, resource_file):
        """
        Checks if resource_file exists in the given system's temp directory.
        :param resource_file: str
        :return: bool
        """
        return os.path.isfile(self._create_resource_path(resource_file))

    def _run_transformers(self):
        """
        Runs all the transformer methods listed providing the MongoDB client context instance.
        """
        with MongoClientContext(self._mongo_client_ctx) as client:
            self._create_dictionary(client)
            self._create_lsi_similarity_index(client)

    def _create_dictionary(self, mongo_client):
        """
        Creates the gensim Dictionary (gensim.corpora.dictionary.Dictionary) or loads it if it already exists and sets
        the object's dictionary property.
        :param mongo_client: server.db.MongoClientContext
        """
        from gensim.corpora.dictionary import Dictionary

        if self._resource_exists(self.dictionary_file):
            self.logger().debug(
                    "Dictionary file found, loading it [%s]" % self._create_resource_path(self.dictionary_file))
            self._dictionary = Dictionary.load(self._create_resource_path(self.dictionary_file))
        else:
            self.logger().debug("Dictionary file not found, creating a new Dictionary file")
            self._dictionary = Dictionary()

        documents = []
        for doc in [di for d in mongo_client.scrappers_collections() for di in d.find()]:
            documents.append(self.tokenize_sentence(doc[self.considerable_doc_property]))

        self.logger().debug("Adding %d documents to dictionary (will skip existing ones)" % len(documents))
        self._dictionary.add_documents(documents)
        self._dictionary.save(self._create_resource_path(self.dictionary_file))

    def _create_lsi_similarity_index(self, mongo_client):
        """
        Creates a Similarity index based on LSI model from the available dictionary. Sets the object's lsi_model and
        similarity_index object properties.
        """
        from gensim.models import LsiModel
        from gensim.similarities import MatrixSimilarity

        self._lsi_mapping.clear()
        bow_corpus = []
        for idx, tp in enumerate([(c, di) for c in mongo_client.scrappers_collections() for di in c.find()]):
            self._lsi_mapping[idx] = tp
            bow_corpus.append(self.sentence_to_bow(tp[1][self.considerable_doc_property]))

        self._lsimodel = LsiModel(bow_corpus, id2word=self.dictionary)
        self._sim_index = MatrixSimilarity(self._lsimodel[bow_corpus])

    def calculate_similarities(self):
        """
        Find / calculate similarities between documents in the index.
        Returns a defaultdict with the key as the LSI index and the value is a list of tuples with the following values
        (LSI model Index, similarity threshold - numpy.float32)
        tuple
        :return: defaultdict(list)
        """
        similarities = defaultdict(list)
        if not self.lsi_index_mapping:
            return

        for idx, tp in sorted(self.lsi_index_mapping.items(), key=itemgetter(0)):
            sentence = tp[1][self.considerable_doc_property]
            bow = self.sentence_to_bow(sentence)
            latent_space_vector = self.lsi_model[bow]
            sim_vector = self.similarity_index[latent_space_vector]
            sorted_mapped_vector = list(sorted(enumerate(sim_vector), key=itemgetter(1)))
            for sit in [v for v in sorted_mapped_vector if
                        v[0] != idx and v[1] >= self.similarity_threshold and tp[0].name !=
                                self.lsi_index_mapping[v[0]][0].name]:
                if sit[0] not in similarities:
                    similarities[idx].append(sit)

        # for s in similarities.items():
        #     main_sentence = self.lsi_index_mapping[s[0]][1][self.considerable_doc_property]
        #     print("[%s] %s:" % (self.lsi_index_mapping[s[0]][0].name, main_sentence))
        #     for sm in s[1]:
        #         print("\t[%f][%s]: %s" % (sm[1], self._lsi_mapping[sm[0]][0].name,
        #                                   self.lsi_index_mapping[sm[0]][1][self.considerable_doc_property]))
        return similarities

    def tokenize_sentence(self, sentence):
        """
        Tokenize a sentence (see 'tokenized_corpus_sentences' method on what tokenization in this context means).
        :param sentence: str
        :return: a list
        """
        excluded = set(chain(self._stopwords, string.punctuation))
        return [w.lower() for w in word_tokenize(sentence) if w.lower() not in excluded]

    def sentence_to_bow(self, sentence):
        """
        Transforms a string sentence to a VSM bag-of-words representation.
        :param sentence: str
        :return: list of tuples
        """
        return self.dictionary.doc2bow(self.tokenize_sentence(sentence))
