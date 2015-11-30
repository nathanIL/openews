from scrappers.plugins.reuters import Reuters
import nose.tools
import unittest
import os
import os.path
import validators
import httpretty
from unittest.mock import MagicMock


class TestReuters(unittest.TestCase):
    def setUp(self):
        self._scrapper = Reuters()
        self._fixture = 'reuters'
        self._data = self.mock_resource_urls()

        self._scrapper.resource_urls = MagicMock(return_value=self._data)

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
        self.assertIsInstance(self._scrapper, Reuters)

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
        self._scrapper._titles_count = 10
        self.assertEqual(len(self._scrapper.scrape_resources().get('categories')), self._scrapper.titles_count)
        self._scrapper._titles_count = 35
        self.assertEqual(len(self._scrapper.scrape_resources().get('categories')), self._scrapper.titles_count)

    @httpretty.activate
    def test_call_(self):
        for resource in self._scrapper.resource_urls():
            httpretty.register_uri(httpretty.GET, resource['url'],
                                   body=resource['data'], content_type=resource['mime'])

        final_scraped_document = self._scrapper()

    @nose.tools.nottest
    def real_test(self):
        s = Reuters()
        s()