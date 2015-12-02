"""
Some utilities, ABCs and other base classes used in the testing phase.
"""
import nose.tools
import os
import os.path
import httpretty
import abc
import mongomock


class ScrapperTestCase(metaclass=abc.ABCMeta):
    def create_scrapper_instance(self, *args, **kwargs):
        klass = self.scrapper_class(*args, **kwargs)
        return klass(mongo_client_class=mongomock.MongoClient)

    @abc.abstractproperty
    def scrapper_class(self):
        """
        Test cases must implement this and return the test scrapper class
        :return: a test scrapper class.
        """
        pass


class RSSTestCase(ScrapperTestCase):
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
    def test_scrape_resource(self):
        for resource in self._scrapper.resource_urls():
            httpretty.register_uri(httpretty.GET, resource['url'],
                                   body=resource['data'], content_type=resource['mime'])

        data = self._scrapper.scrape_resources()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data.keys()), 1)
        self.assertTrue('categories' in data)

    @httpretty.activate
    def test_titles_count(self):
        for resource in self._scrapper.resource_urls():
            httpretty.register_uri(httpretty.GET, resource['url'],
                                   body=resource['data'], content_type=resource['mime'])
        for cnt in self._title_counts:
            self._scrapper._titles_count = cnt
            self.assertEqual(len(self._scrapper.scrape_resources().get('categories')), self._scrapper.titles_count)

    @httpretty.activate
    def test_call_(self):
        for resource in self._scrapper.resource_urls():
            httpretty.register_uri(httpretty.GET, resource['url'],
                                   body=resource['data'], content_type=resource['mime'])

        self._scrapper()

    @nose.tools.nottest
    def real_test(self):
        s = self.scrapper_class()
        s()
