"""
A Scrapper instance is an entity that collects data from the resources.
"""
import abc
import requests
import gevent
import gevent.monkey
import pymongo
import pymongo.errors
import logging
import urllib3
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from textblob import TextBlob
from server.db import MongoClientContext, MongoConnectionRecord
from server import server_app

gevent.monkey.patch_socket()


class Scrapper(metaclass=abc.ABCMeta):
    """
    Scrappers Abstract Base Class.
    All scrappers must inherit and implement required methods, etc.
    """

    # TODO: Use 'PYTHONWARNINGS' env to disable SSL warnings(??): https://urllib3.readthedocs.org/en/latest/security.html

    def __init__(self, titles_count=None, *args, **kwargs):
        """
        :param titles_count: How many titles to scrape from each source. None is all available.
        :param mongo_client_class: The MongoDB client class. defaults to MongoClient (so we can inject this if needed - unit testing for instance)
        :param args:
        :param kwargs:
        :return:
        """
        super().__init__(*args, **kwargs)
        self._mongo_conn_rec = MongoConnectionRecord(host=server_app.config['MONGO_HOST'],
                                                     port=server_app.config['MONGO_PORT'],
                                                     connect=False)
        self._titles_count = titles_count
        self._skipped_titles = set()
        self.logger().debug("Creating: %s", self)

    @property
    def mongo_connection_record(self):
        return self._mongo_conn_rec

    @staticmethod
    def logger():
        """
        Scrapper's specific logger instance. Use this to log inside scrappers.
        :return: Returns a logging.Logger('openews.scrappers') instance.
        """
        return logging.getLogger('openews.scrappers')

    @staticmethod
    def disabled():
        """
        If this scrapper is disabled or not.
        :return: True or False
        """
        return False

    @property
    def skipped_titles(self):
        """The skipped titles set.
        :return: a set() object holding the skipped titles
        """
        return set(self._skipped_titles)

    def skipping_rules(self, title):
        """
       This method is called by 'should_skip_scrape' and receives the scraped news title, it then decides whether to
       scrape it or not based on the provided rules in this method.
       Some sources have some "noise" news, such as country profiles and such, we don't need these.
       It should optionally be overridden by classes want to exclude some titles from a scraped resource.
       :param title: the title (str) of the scraped resource.
       :return: True in case we are skipping this news, False otherwise.
       """
        return False

    def should_skip_scrape(self, title):
        if self.skipping_rules(title):
            self._skipped_titles.add(title)
            return True
        else:
            return False

    @property
    def titles_count(self):
        """
        We refer to "title" as an atomic sentence to be retrieved. For instance, a forum thread subject.
        :return: The max number (int) of titles to scrape from the source or None for all (default).
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
        if not self.should_translate():
            return data
        for elem in data:
            elem['title_en'] = TextBlob(elem['title']).translate(to='en')

        return data

    def get_resources(self, resources):
        """
        Performs the HTTP request to the provided resource.
        :param resources: return value of 'resource_urls' method.
        :return: a list of dicts ('data': requests.Response, category: str).
        """
        def composite_request(url, category):
            retries = 0
            result = None

            urllib3.disable_warnings()
            while retries <= 10:
                try:
                    self.logger().debug("GETting resource: %s" % url)
                    response = requests.get(url, verify=False)
                    result = {'response': response, 'category': category}
                    break
                except (ConnectionError, Timeout, TooManyRedirects):
                    retries += 1
                    gevent.sleep(5)
                    self.logger().exception("Could not GET resource: %s" % url)

            return result

        threads = [gevent.spawn(composite_request, r['url'], r['category']) for r in resources]
        gevent.joinall(threads)
        return [{'data': t.value['response'], 'category': t.value['category']} for t in threads if t.value is not None]

    def _store_to_db(self, documents):
        """
        Internal utility method to store data in the database
        """
        # TODO: Catch more specific exceptions (??)
        inserted = []
        with MongoClientContext(self.mongo_connection_record) as client:
            scrappers_db = client.scrappers_db()
            if self.__class__.__name__.lower() not in client.database_names():
                self.logger().debug("Creating unique index [%s] on: %s", 'title', self.__class__.__name__.lower())
                scrappers_db[self.__class__.__name__.lower()].create_index([('title', pymongo.ASCENDING)], unique=True)
            for doc in documents['categories']:
                try:
                    self.logger().debug("[%s]: Inserting document: %s", self.__class__.__name__.lower(), doc)
                    inserted.append(scrappers_db[self.__class__.__name__.lower()].insert(doc))
                except pymongo.errors.DuplicateKeyError:
                    self.logger().debug("[%s]: Document [%s] already exists, skipping", self.__class__.__name__.lower(),
                                        doc)
                    pass
                except pymongo.errors.PyMongoError:
                    raise

        return inserted

    def __str__(self):
        return '<<{0}(titles_count={1}, should_translate={2}, encoding={3}, resources={4})>>' \
            .format(self.__class__.__name__,
                    self.titles_count or 'All',
                    self.should_translate(),
                    self.encoding(),
                    ','.join([e['url'] for e in self.resource_urls()]))

    def __call__(self, *args, **kwargs):
        """
        This is called by RQ workers and performs the real work: scrape, normalization, and stores to DB.
        :param args:
        :param kwargs:
        :return: the insert documents
        """
        import log
        transformed_data = self.translate_data(self.scrape_resources())
        transformed_data['scrapper'] = self.__class__.__name__
        return self._store_to_db(transformed_data)
