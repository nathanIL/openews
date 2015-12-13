"""
Some utilities, ABCs and other base classes used in the testing phase.
"""
import nose.tools
import os
import os.path
import httpretty
import abc
import mongomock
import server.db
import log

server.db.MONGO_CLIENT_CLASS = mongomock.MongoClient


class ScrapperTestCase(metaclass=abc.ABCMeta):
    def create_scrapper_instance(self, *args, **kwargs):
        klass = self.scrapper_class(*args, **kwargs)
        return klass()

    @abc.abstractproperty
    def scrapper_class(self):
        """
        Test cases must implement this and return the test scrapper class
        :return: a test scrapper class.
        """
        pass

    def test_disabled(self):
        self.assertIsInstance(self.create_scrapper_instance().disabled(), bool)


class RSSTestCase(ScrapperTestCase):
    """
    A mixin to be used by any RSS based scrapper test.
    """

    @nose.tools.nottest
    def mock_resource_urls(self):
        data = []
        dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', self._fixture)
        for file in [os.path.join(dirname, f) for f in os.listdir(dirname)]:
            basename = os.path.basename(file)
            data.append({'category': os.path.splitext(basename)[0],
                         'url': 'http://test.com/rss/%s/%s' % (self._fixture, basename),
                         'mime': 'text/xml',
                         'data': ''.join(open(file, encoding=self._scrapper.encoding()).readlines())})
        return data

    def test_scrapper_instance(self):
        self.assertIsInstance(self._scrapper, self.scrapper_class())

    @httpretty.activate
    def test_run_http_mocked_tests(self):
        """Executed HTTP mocked tests"""
        for resource in self._scrapper.resource_urls():
            httpretty.register_uri(httpretty.GET, resource['url'],
                                   body=resource['data'], content_type=resource['mime'])

        scrape_resouces_data = self._scrapper.scrape_resources()
        call_resouces_data = self._scrapper()
        self.assertIsInstance(scrape_resouces_data, dict, "Is 'scrape_resouces' returns a dict object?")
        self.assertEqual(len(scrape_resouces_data.keys()), 1,
                         "Is 'scrape_resouces' returns a dict object with a single key?")
        self.assertIn('categories', scrape_resouces_data, "Is 'scrape_resouces' return dict has a 'categories' key?")
        self.assertIsInstance(call_resouces_data, list, "Is __call__() returns a list object?")
        self.assertGreater(len(call_resouces_data), 0, "Is __call__() returns a non empty list object?")
        for cnt in self._title_counts:
            self._scrapper._titles_count = cnt
            scrape_cnt_count_resouces_data = self._scrapper.scrape_resources()
            self.assertEqual(len(scrape_cnt_count_resouces_data.get('categories')), self._scrapper.titles_count,
                             "Is titles count equals to tested count [{0}]?".format(cnt))
        self.assertIsInstance(self._scrapper.skipped_titles, set, "Is 'skipped_titles' returns a set object?")
        # If our scrapper actually implements 'skipping_rules' property, then it must has rules.
        if 'skipping_rules' in self._scrapper.__class__.__dict__:
            self.assertGreater(len(self._scrapper.skipped_titles), 0,
                               "Is 'skipped_titles' have titles in it? (should have in this case)")
        else:
            self.assertEqual(len(self._scrapper.skipped_titles), 0,
                             "Is 'skipped_titles' return count is == 0?")

