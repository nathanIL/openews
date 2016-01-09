import pymongo
import logging
from pymongo import MongoClient
from collections import namedtuple, defaultdict
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

    def scrappers_db(self):
        """
        The scrappers database (holds data scrapped by scrappers).
        :return: pymongo.database.Database
        """
        return self[server_app.config['MONGO_SCRAPPERS_DB']]

    def similarities_db(self):
        """
        The similarities database (holds similar scrapper documents).
        :return: pymongo.database.Database
        """
        return self[server_app.config['MONGO_SIMILARITIES_DB']]

    def scrappers_collections(self):
        """
        Returns the scrapper collections.
        :return: a list of pymongo.collection.Collection
        """
        from scrappers.utils import scrapper_classes
        scrapper_classes_names = set([c.__name__.lower() for c in scrapper_classes()])
        collections = []
        for scrapper_collection in [s for s in self.scrappers_db().collection_names(include_system_collections=False) if
                                    s in scrapper_classes_names]:
            collections.append(self.scrappers_db().get_collection(scrapper_collection))
        return collections

    def scrappers_collections_statistics(self):
        """
        Scrappers database collections statistics
        :return: defaultdict
        """
        results = defaultdict(dict)
        for collection in self.scrappers_collections():
            total_documents_count = collection.count()
            bundled_documents_count = collection.find({'bundled': {'$exists': True}}).count()
            results[collection.name]['documents_count'] = total_documents_count
            results[collection.name]['similar'] = bundled_documents_count
            results[collection.name]['last_scrapped_at'] = collection.find().sort('scraped_at',
                                                                                  pymongo.DESCENDING)[0]['scraped_at']
        return results

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
