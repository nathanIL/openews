from nltk.probability import FreqDist
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

    @property
    def nltk_corpus(self):
        return self._nltk_corpus

    @property
    def stopwords(self):
        return self._stopwords

    def corpus_to_tokenized_documents(self):
        """
        Creates a list of tokenized documents from the nltk.corpus
        :param corpus:
        :return: a list of tokenized documents
        """
        stops = set([w.lower() for w in self.stopwords])
        freq_dist = FreqDist()
        documents = []

        for sentence in self.nltk_corpus.sents():
            document = []
            for word in [w.lower() for w in sentence if w.lower() not in stops]:
                freq_dist[word] += 1
                if freq_dist[word] > 1:
                    document.append(word)
            documents.append(document)
        return documents
