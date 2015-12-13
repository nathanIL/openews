import pymongo
import logging
from pymongo import MongoClient
from collections import namedtuple

MONGO_CLIENT_CLASS = MongoClient
MongoConnectionRecord = namedtuple('MongoConnectionRecord', ['host', 'port', 'connect'])
RedisConnectionRecord = namedtuple('RedisConnectionRecord', ['host', 'port'])


class MongoClientContext(object):
    """
    A Context manager class to deal with MongoClient related database (based on the config parameters).
    """

    def __init__(self, mongo_conn_red):
        self.logger.debug("Initializing MongoClient instance")
        self._client = MONGO_CLIENT_CLASS(**mongo_conn_red._asdict())

    @property
    def logger(self):
        return logging.getLogger('openews.scrappers')

    def __enter__(self):
        return self._client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is pymongo.errors.AutoReconnect:
            self.logger.warning("MongoDB AutoReconnect warning: %s", exc_val)
        elif exc_type is pymongo.errors.ConnectionFailure:
            self.logger.fatal("MongoDB Connection Failure: %s" % exc_val)

        self._client.close()
        return False
