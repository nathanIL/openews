import mongomock
import unittest
import server.db
import datetime
import random
from server.db import MongoClientContext, MongoConnectionRecord
from server import server_app
from language.utils import stats
import log

server.db.MONGO_CLIENT_CLASS = mongomock.MongoClient


class TestLanguageUtils(unittest.TestCase):
    """A test class for the language.utils module"""

    def setUp(self):
        self._mongo_conn_rec = MongoConnectionRecord(host='localhost', port='27017', connect=False)
        self._mongo_raw_dbname = server_app.config['MONGO_RAW_COLLECTION']
        now = datetime.datetime.utcnow()
        self._sample_documents = {'bbc': [
            {"url": "http://www.bbc.co.uk/news/magazine-35092589#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
             "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
             "title": "Should you rent your Christmas tree?"},
            {
                "url": "http://www.bbc.co.uk/news/blogs-magazine-monitor-35130983#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
                "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
                "title": "10 things we didn't know last week"},
            {"url": "http://www.bbc.co.uk/news/magazine-35123180#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
             "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
             "title": "Quiz of the week's news"},
            {
                "url": "http://www.bbc.co.uk/news/science-environment-35115195#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
                "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
                "title": "200-year-old fossil mystery resolved"},
            {"url": "http://www.bbc.co.uk/news/magazine-35121320#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
             "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
             "title": "Waiting 56 years for my sister"},
            {"url": "http://www.bbc.co.uk/news/magazine-35110421#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
             "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
             "title": "Why do people resent buy-to-letters so much?"},
            {"url": "http://www.bbc.co.uk/news/in-pictures-35120594#sa-ns_mchannel=rss&ns_source=PublicRSS20-sa",
             "category": "Top Stories", "scraped_at": now + datetime.timedelta(days=random.randint(0, 55)),
             "title": "Week in pictures"}],
            'ynetnews': [{"category": "All News",
                          "title": "Israel losing fight against 'Facebook jihad'",
                          "url": "http://www.ynetnews.com/articles/0,7340,L-4738256,00.html",
                          "scraped_at": now + datetime.timedelta(days=random.randint(0, 55))},
                         {"category": "All News",
                          "bundled": True,
                          "title": "Meir Ettinger: The face of Jewish terrorism",
                          "url": "http://www.ynetnews.com/articles/0,7340,L-4738049,00.html",
                          "scraped_at": now + datetime.timedelta(days=random.randint(0, 55))},
                         {"category": "All News",
                          "title": "A night spent fighting terror",
                          "url": "http://www.ynetnews.com/articles/0,7340,L-4738132,00.html",
                          "scraped_at": now + datetime.timedelta(days=random.randint(0, 55))},
                         {"category": "All News",
                          "title": "Online store tells customer: 'We don't sell to Arabs'",
                          "url": "http://www.ynetnews.com/articles/0,7340,L-4733519,00.html",
                          "scraped_at": now + datetime.timedelta(days=random.randint(0, 55))},
                         {"category": "All News",
                          "bundled": True,
                          "title": "Erekat visits family of PA security officer who hurt 2 in terror attack",
                          "url": "http://www.ynetnews.com/articles/0,7340,L-4735110,00.html",
                          "scraped_at": now + datetime.timedelta(days=random.randint(0, 55))},
                         {"category": "All News",
                          "title": "NIS 400,000 raised in two weeks for synagogue in memory of slain teen",
                          "url": "http://www.ynetnews.com/articles/0,7340,L-4733527,00.html",
                          "scraped_at": now + datetime.timedelta(days=random.randint(0, 55))}]}

    def _load_docs(self, mc):
        for sd in self._sample_documents:
            mc[self._mongo_raw_dbname][sd].insert_many(self._sample_documents[sd])

    def test_stats(self):
        """Test language.utils.stats method"""
        with MongoClientContext(self._mongo_conn_rec) as mc:
            self._load_docs(mc)
            statistics = stats(mc)
            self.assertIsInstance(statistics, dict, "Is stats return value a dict?")
            for collection in statistics:
                self.assertSetEqual(set(['documents_count',
                                         'last_scrapped_at',
                                         'bundled']), set(statistics[collection].keys()), "Are stats keys valid")
