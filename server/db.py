import pymongo
import logging
from pymongo import MongoClient
from collections import namedtuple
from server import server_app

MONGO_CLIENT_CLASS = MongoClient
MongoConnectionRecord = namedtuple('MongoConnectionRecord', ['host', 'port', 'connect'])
RedisConnectionRecord = namedtuple('RedisConnectionRecord', ['host', 'port'])


class MongoClientContext(object):
    """
    A Context manager class to deal with MongoClient related database (based on the config parameters).
    """

    def __init__(self, mongo_conn_red):
        self.logger.debug("Initializing MongoClient instance with class: %s" % MONGO_CLIENT_CLASS)
        self._client = MONGO_CLIENT_CLASS(**mongo_conn_red._asdict())

    @property
    def logger(self):
        return logging.getLogger('openews.server')

    def __getattr__(self, name):
        """
        We delegate to not found attributes to MongoClient.
        :param name:
        :return:
        """
        return getattr(self._client, name)

    def raw_db(self):
        """
        The RAW database
        :return: pymongo.database.Database
        """
        return self[server_app.config['MONGO_RAW_COLLECTION']]

    def scrappers_collections(self):
        """
        Returns the scrapper collections.
        :return: a list of pymongo.collection.Collection
        """
        from scrappers.utils import scrapper_classes
        scrapper_classes = set([c.__name__.lower() for c in scrapper_classes()])
        collections = []
        for scrapper_collection in [s for s in self.raw_db().collection_names(include_system_collections=False) if
                                    s in scrapper_classes]:
            collections.append(self.raw_db().get_collection(scrapper_collection))
        return collections

    def __getitem__(self, item):
        """
        We delegate to not found items to MongoClient.
        :param item:
        :return:
        """
        return getattr(self._client, item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is pymongo.errors.AutoReconnect:
            self.logger.warning("MongoDB AutoReconnect warning: %s", exc_val)
        elif exc_type is pymongo.errors.ConnectionFailure:
            self.logger.fatal("MongoDB Connection Failure: %s" % exc_val)

        self._client.close()
        return False
