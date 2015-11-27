"""
A Scrapper instance is an entity that collects data from the resources.
"""
import abc
import requests
import sys
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from server import server_app


class Scrapper(metaclass=abc.ABCMeta):
    """
    Scrappers Abstract Base Class.
    All scrappers must inherit and implement required methods, etc.
    """

    def __init__(self, titles_count=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._titles_count = titles_count

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
        :return: a list holding the scraped titles as dict values (title, url) as keys
        """
        pass

    def get_resource(self, resource):
        return requests.get(resource, verify=False)

    def __call__(self, *args, **kwargs):
        """
        This is called by RQ and performs the scrape, normalization, and stores to DB.
        :param args:
        :param kwargs:
        :return:
        """
        try:
            raw = MongoClient(host=server_app.config['MONGO_HOST'], port=server_app.config['MONGO_PORT'])[
                server_app.config['MONGO_RAW_COLLECTION']]
            scraped_data = self.scrape_resource()
        except PyMongoError as me:
            print("[MongoDB][Fatal Error]: %s" % me, file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            pass
