import unittest
import os
from server.db import MongoClientContext
from server import server_app
from manager import mongo_connection_record
from language.utils import stats


@unittest.skipIf(os.environ.get('TRAVIS', None) is not None, "Skipping in Travis CI builds")
class TestLanguageUtils(unittest.TestCase):
    """A test class for the language.utils module"""

    def setUp(self):
        self._mongo_raw_dbname = server_app.config['MONGO_RAW_COLLECTION']

    def test_stats(self):
        """Test language.utils.stats method"""
        with MongoClientContext(mongo_connection_record) as mc:
            statistics = stats(mc)
            self.assertIsInstance(statistics, dict, "Is stats return value a dict?")
            for collection in statistics:
                self.assertSetEqual(set(['documents_count',
                                         'last_scrapped_at',
                                         'bundled']), set(statistics[collection].keys()), "Are stats keys valid")
