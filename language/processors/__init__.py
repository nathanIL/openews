from nltk.tokenize import word_tokenize
from server.db import MongoClientContext
from operator import itemgetter
from server import server_app
import tempfile
import os
import nltk
import logging

nltk.data.path.append('nltk_data')


class Transformer(object):
    """
    Transforms the scrapped texts (aka the corpus) to to a dictionary and various models (mostly VSM based like LSI).
    """

    def __init__(self, mongo_client_ctx, stopwords):
        self._stopwords = stopwords
        self._mongo_client_ctx = mongo_client_ctx
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
    def dictionary_file(self):
        return "openews.processors.dict"

    @property
    def stopwords(self):
        """
        Stopwords list as provided in the constructor.
        :return: a list of stopwords
        """
        return self._stopwords

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
            print(self.dictionary)
            #self.__create_lsi_model(client)

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
            documents.append(self.tokenize_sentence(doc['title']))

        self.logger().debug("Adding %d documents to dictionary (will skip existing ones)" % len(documents))
        self._dictionary.add_documents(documents)
        self._dictionary.save(self._create_resource_path(self.dictionary_file))

    def _create_lsi_model(self, mongo_client):
        """
        Creates the LSI model from the available dictionary. Sets the object's lsi_model property.
        """
        from gensim.models import LsiModel

        bow_corpus = []
        mapping = dict()
        for collection in mongo_client.scrappers_collections():
            for doc in collection.find():
                bow_corpus.append(self.sentence_to_bow(doc['title']))
                mapping[len(bow_corpus) - 1] = doc['title']

        self._lsimodel = LsiModel(bow_corpus, id2word=self.dictionary)

            # from gensim.similarities import MatrixSimilarity
            # index = MatrixSimilarity(self._lsimodel[bow_corpus])

            # with MongoClientContext(self._mongo_client_ctx) as client:
            #     raw = client.raw_db()
            #     for collection in raw.collection_names(include_system_collections=False):
            #         for doc in raw[collection].find():
            #             simed = sorted(list(enumerate(index[self._lsimodel[self.sentence_to_bow(doc['title'])]])), key=itemgetter(1))
            #             print("[{0}]: {1} ==> {2}".format(simed[-2][1], doc['title'], mapping[simed[-2][0]]))


            # self._lsimodel.save(self._create_resource_path(server_app.config['GENSIM_DICT_FILE']))
            # print(self._lsimodel.show_topics(formatted=True))
            # print(self._lsimodel[self.sentence_to_bow("terror attack")])
            # from operator import itemgetter
            # print(sorted(list(enumerate(index[self._lsimodel[self.sentence_to_bow("The NBA player set to get a Chinese green card")]])), key=itemgetter(1)))
            # print(mapping[43])

    def tokenize_sentence(self, sentence):
        """
        Tokenize a sentence (see 'tokenized_corpus_sentences' method on what tokenization in this context means).
        :param sentence: str
        :return: a list
        """
        return [w.lower() for w in word_tokenize(sentence) if w.lower() not in self.stopwords]

    def sentence_to_bow(self, sentence):
        """
        Transforms a string sentence to a VSM bag-of-words representation.
        :param sentence: str
        :return: list of tuples
        """
        return self.dictionary.doc2bow(self.tokenize_sentence(sentence))

# class Similarity(object):
#     def __init__(self, nltk_corpus, stopwords):
#         """
#         Creates a similarity class.
#         :param nltk_corpus: an nltk.corpus instance
#         :param stopwords: an iterable holding a list of stop-words
#         :return:
#         """
#         self._nltk_corpus = nltk_corpus
#         self._stopwords = stopwords
#         self._tokenized_sentences = []
#         self._dictionary = None
#         self._tfidf_model = None
#
#     @property
#     def tokenized_corpus_sentences(self):
#         """
#         Returns (or creates if not already created / called) a list of tokenized documents from the loaded nltk.corpus.
#         By tokenized, I mean, remove stop-words, and words that their frequency distribution is 1.
#         :return: list
#         """
#         if not self._tokenized_sentences:
#             stops = set([w.lower() for w in self.stopwords])
#             freq_dist = FreqDist()
#
#             for sentence in self._nltk_corpus.sents():
#                 document = []
#                 for word in [w.lower() for w in sentence if w.lower() not in stops]:
#                     freq_dist[word] += 1
#                     if freq_dist[word] > 1:
#                         document.append(word)
#                 self._tokenized_sentences.append(document)
#
#         return self._tokenized_sentences
#
#     @property
#     def dictionary(self):
#         """
#         A dictionary of the loaded corpus make from the tokenized sentences.
#         :return: gensim.corpora.dictionary.Dictionary instance
#         """
#         from gensim.corpora.dictionary import Dictionary
#         if self._dictionary is None:
#             self._dictionary = Dictionary(self.tokenized_corpus_sentences)
#
#         return self._dictionary
#
#     @property
#     def stopwords(self):
#         """
#         Stopwords list as provided in the constructor.
#         :return: a list of stopwords
#         """
#         return self._stopwords
#
#     def tokenize_sentence(self, sentence):
#         """
#         Tokenize a sentence (see 'tokenized_corpus_sentences' method on what tokenization in this context means).
#         :param sentence: str
#         :return: a list
#         """
#         return [w.lower() for w in word_tokenize(sentence) if w.lower() not in self.stopwords]
#
#     def trasform_to_tfidf_model(self):
#         """
#          TF-IDF model transformation with for loaded training corpus.
#         :return: gensim.models.tfidfmodel.TfidfModel instance
#         """
#         from gensim.models import TfidfModel
#         if self._tfidf_model is None:
#             self._tfidf_model = TfidfModel(dictionary=self.dictionary)
#
#         return self._tfidf_model
#
#     def sentence_to_bow(self, sentence):
#         """
#         Transforms a string sentence to a VSM bag-of-words representation.
#         :param sentence: str
#         :return: list of tuples
#         """
#         return self.dictionary.doc2bow(self.tokenize_sentence(sentence))
