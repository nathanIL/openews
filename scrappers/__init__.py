"""
A Scrapper instance is an entity that collects data from the resources.
"""
import abc
import requests
import sys
import gevent
import gevent.monkey
import pymongo
import pymongo.errors
import logging
from textblob import TextBlob
from pymongo import MongoClient
from server import server_app

gevent.monkey.patch_socket()


class Scrapper(metaclass=abc.ABCMeta):
    """
    Scrappers Abstract Base Class.
    All scrappers must inherit and implement required methods, etc.
    """

    # TODO: Use 'PYTHONWARNINGS' env to disable SSL warnings(??): https://urllib3.readthedocs.org/en/latest/security.html

    def __init__(self, titles_count=None, mongo_client_class=MongoClient, *args, **kwargs):
        """
        :param titles_count: How many titles to scrape from each source. None is all available.
        :param mongo_client_class: The MongoDB client class. defaults to MongoClient (so we can inject this if needed - unit testing for instance)
        :param args:
        :param kwargs:
        :return:
        """
        super().__init__(*args, **kwargs)
        self._titles_count = titles_count
        self._mongo_client_class = mongo_client_class
        self._skipped_titles = set()
        self.logger().debug("Creating: %s", self)

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

    @staticmethod
    def get_resources(resources):
        """
        Performs the HTTP request to the provided resource.
        :param resources: return value of 'resource_urls' method.
        :return: a list of dicts ('data': requests.Response, category: str).
        """
        # TODO: Once a request fails, re-queue it for another try.
        def composite_request(url, category):
            return {'response': requests.get(url, verify=False), 'category': category}

        threads = [gevent.spawn(composite_request, r['url'], r['category']) for r in resources]
        gevent.joinall(threads)
        return [{'data': t.value['response'], 'category': t.value['category']} for t in threads]

    def _store_to_db(self, documents):
        """
        Internal utility method to store data in the database
        """
        # TODO: Catch more specific exceptions (??)
        inserted = []
        try:
            client = self._mongo_client_class(host=server_app.config['MONGO_HOST'],
                                              port=server_app.config['MONGO_PORT'])
            raw_db = client[server_app.config['MONGO_RAW_COLLECTION']]
            if self.__class__.__name__.lower() not in client.database_names():
                self.logger().debug("Creating unique index [%s] on: %s", 'url', self.__class__.__name__.lower())
                raw_db[self.__class__.__name__.lower()].create_index([('url', pymongo.ASCENDING)], unique=True)
            for doc in documents['categories']:
                try:
                    self.logger().debug("[%s]: Inserting document: %s", self.__class__.__name__.lower(), doc)
                    inserted.append(raw_db[self.__class__.__name__.lower()].insert(doc))
                except pymongo.errors.DuplicateKeyError:
                    self.logger().debug("[%s]: Document [%s] already exists, skipping", self.__class__.__name__.lower(),
                                        doc)
                    pass
                except pymongo.errors.PyMongoError:
                    raise
        except pymongo.errors.AutoReconnect as e:
            self.logger().warning("MongoDB AutoReconnect warning: %s", e)
        except pymongo.errors.ConnectionFailure as e:
            self.logger().exception("MongoDB Connection Failure")
            sys.exit(1)
        finally:
            return inserted

    def __str__(self):
        return '<<{0}(titles_count={1}, mongo_client_class={2}, should_translate={3}, encoding={4}, resources={5})>>' \
            .format(self.__class__.__name__,
                    self.titles_count or 'All',
                    self._mongo_client_class,
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
        transformed_data = self.translate_data(self.scrape_resources())
        transformed_data['scrapper'] = self.__class__.__name__
        return self._store_to_db(transformed_data)
