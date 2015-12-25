from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import nltk

nltk.data.path.append('nltk_data')


class Similarity(object):
    def __init__(self, nltk_corpus, stopwords):
        """
        Creates a similarity class.
        :param nltk_corpus: an nltk.corpus instance
        :param stopwords: an iterable holding a list of stop-words
        :return:
        """
        self._nltk_corpus = nltk_corpus
        self._stopwords = stopwords
        self._tokenized_sentences = []
        self._dictionary = None
        self._tfidf_model = None

    @property
    def tokenized_corpus_sentences(self):
        """
        Returns (or creates if not already created / called) a list of tokenized documents from the loaded nltk.corpus.
        By tokenized, I mean, remove stop-words, and words that their frequency distribution is 1.
        :return: list
        """
        if not self._tokenized_sentences:
            stops = set([w.lower() for w in self.stopwords])
            freq_dist = FreqDist()

            for sentence in self._nltk_corpus.sents():
                document = []
                for word in [w.lower() for w in sentence if w.lower() not in stops]:
                    freq_dist[word] += 1
                    if freq_dist[word] > 1:
                        document.append(word)
                self._tokenized_sentences.append(document)

        return self._tokenized_sentences

    @property
    def dictionary(self):
        """
        A dictionary of the loaded corpus make from the tokenized sentences.
        :return: gensim.corpora.dictionary.Dictionary instance
        """
        from gensim.corpora.dictionary import Dictionary
        if self._dictionary is None:
            self._dictionary = Dictionary(self.tokenized_corpus_sentences)

        return self._dictionary

    @property
    def stopwords(self):
        """
        Stopwords list as provided in the constructor.
        :return: a list of stopwords
        """
        return self._stopwords

    def tokenize_sentence(self, sentence):
        """
        Tokenize a sentence (see 'tokenized_corpus_sentences' method on what tokenization in this context means).
        :param sentence: str
        :return: a list
        """
        return [w.lower() for w in word_tokenize(sentence) if w.lower() not in self.stopwords]

    def trasform_to_tfidf_model(self):
        """
         TF-IDF model transformation with for loaded training corpus.
        :return: gensim.models.tfidfmodel.TfidfModel instance
        """
        from gensim.models import TfidfModel
        if self._tfidf_model is None:
            self._tfidf_model = TfidfModel(dictionary=self.dictionary)

        return self._tfidf_model

    def sentence_to_bow(self, sentence):
        """
        Transforms a string sentence to a VSM bag-of-words representation.
        :param sentence: str
        :return: list of tuples
        """
        return self.dictionary.doc2bow(self.tokenize_sentence(sentence))
