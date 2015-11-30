"""
A Scrapper instance is an entity that collects data from the resources.
"""
import abc
import requests
import sys
import gevent
import gevent.monkey
import os
from textblob import TextBlob
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from server import server_app

gevent.monkey.patch_socket()


class Scrapper(metaclass=abc.ABCMeta):
    """
    Scrappers Abstract Base Class.
    All scrappers must inherit and implement required methods, etc.
    """

    # TODO: Use 'PYTHONWARNINGS' env to disable SSL warnings(??): https://urllib3.readthedocs.org/en/latest/security.html

    def __init__(self, titles_count=None, mongo_client_class=MongoClient, *args, **kwargs):
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
    def encoding(self):
        """
        Data resource encoding
        :return:
        """
        pass

    @abc.abstractproperty
    def resource_urls(self):
        """
        Must be implemented by inheriting class and return a list of dict (category, url) as keys.
        :return: a list of dicts that include (category, url) to start scraping from.
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
    def scrape_resources(self):
        """
        Scrapes the provided resource up to titles_count. It should not raise any Exception.
        :return: a dict with a single key (categories) holding the scraped documents. each document have the following
        structure: {'category': str, 'title': str, 'url': str, 'scraped_at': int, *['title_en': str]}
        * optional field in case the source was translated.
        """
        pass

    def translate_data(self, data):
        """
        This should normalize (translate) the data in case needed (return value of should_translate method).
        :param data: A list with dict values (data returned from scrape_resource method).
        :return: data with added key (title_en) holding the translated data (in case translated has been performed).
        """
        # TODO: Fix for multiple categories (NOT WORKING NOW)
        if not self.should_translate(): return data
        for elem in data:
            elem['title_en'] = TextBlob(elem['title']).translate(to='en')

        return data

    def get_resources(self, resources):
        """
        Performs the HTTP request to the provided resource.
        :param resources: return value of 'resource_urls' method.
        :return: a list of dicts ('data': requests.Response, category: str).
        """
        threads = list()
        for r in resources:
            threads.append({'gthread': gevent.spawn(requests.get, r['url'], verify=False), 'category': r['category']})
        gevent.joinall([t['gthread'] for t in threads])
        return [{'data': r['gthread'].value, 'category': r['category']} for r in threads if
                r['gthread'].ready() and r['gthread'].successful()]

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
            translated_data = self.translate_data(self.scrape_resources())
            translated_data['scrapper'] = self.__class__.__name__
        except PyMongoError as me:
            print("[MongoDB][Fatal Error]: %s" % me, file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(e)
        finally:
            return translated_data
