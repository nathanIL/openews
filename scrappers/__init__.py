"""
A Scrapper instance is an entity that collects data from the resources.
"""
import abc
import requests
import sys
from textblob import TextBlob
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from server import server_app


class Scrapper(metaclass=abc.ABCMeta):
    """
    Scrappers Abstract Base Class.
    All scrappers must inherit and implement required methods, etc.
    """

    def __init__(self, titles_count=10, mongo_client_class=MongoClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._titles_count = titles_count
        self._mongo_client_class = mongo_client_class

    @property
    def titles_count(self):
        """
        We refer to "title" as an atomic sentence to be retrieved.
        For instance, a forum thread subject.
        :return: The max number (int) of titles to scrape from the source.
        """
        return self._titles_count

    @abc.abstractproperty
    def resource_url(self):
        """
        Must be implemented by inheriting class and return the base (parent) source from which we start to scrape.
        :return: string holding a valid URL to start scraping from.
        """
        pass

    @abc.abstractproperty
    def should_translate(self):
        """
        If the resource requires translation to en in order to normalize the data before we pass it to NLP procedures.
        :return:
        """
        pass

    @abc.abstractmethod
    def scrape_resource(self):
        """
        Scrapes the provided resource up to titles_count. It should not raise any Exception.
        :return: a list holding the scraped titles as dict values. (title, url, scraped_at) as keys.
        """
        pass

    def translate_data(self, data):
        """
        This should normalize (translate) the data in case needed (return value of should_translate method).
        :param data: A list with dict values (data returned from scrape_resource method).
        :return: data with added key (title_en) holding the translated data (in case translated has been performed).
        """
        if not self.should_translate(): return data
        for elem in data:
            elem['title_en'] = TextBlob(elem['title']).translate(to='en')

        return data

    def get_resource(self, resource):
        """
        Performs the HTTP request to the provided resource.
        :param resource: a URL to make a request to.
        :return: requests.Response object.
        """
        return requests.get(resource, verify=False)

    def __call__(self, *args, **kwargs):
        """
        This is called by RQ workers and performs the real work: scrape, normalization, and stores to DB.
        :param args:
        :param kwargs:
        :return: the normalized and translated list of documents (list of dicts).
        """
        # TODO: Perform the actual DB update
        translated_data = []
        try:
            raw = self._mongo_client_class(host=server_app.config['MONGO_HOST'], port=server_app.config['MONGO_PORT'])[
                server_app.config['MONGO_RAW_COLLECTION']]
            translated_data = self.translate_data(self.scrape_resource())
            for elem in translated_data:
                elem['scrapper'] = self.__class__.__name__
        except PyMongoError as me:
            print("[MongoDB][Fatal Error]: %s" % me, file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(e)
        finally:
            return translated_data
