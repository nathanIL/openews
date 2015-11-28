from nose.tools import nottest, with_setup, assert_is_instance, \
    assert_true, assert_equal, assert_true
from scrappers.plugins.rotter import Rotter
import os
import validators
import httpretty

rotter_scrapper = None
test_data = None


def create_scrapper_instance():
    global rotter_scrapper
    rotter_scrapper = Rotter()


def create_fake_requests_mock_data():
    global test_data
    html = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rotter1.html')
    test_data = ''.join(open(html, encoding='cp1255').readlines())


@with_setup(create_scrapper_instance)
def test_instance_creation():
    assert_is_instance(rotter_scrapper, Rotter)


@with_setup(create_scrapper_instance)
def test_resource_url():
    assert_true(validators.url(rotter_scrapper.resource_url()))


@httpretty.activate
@with_setup(create_scrapper_instance)
@with_setup(create_fake_requests_mock_data)
def test_scrape_resource():
    httpretty.register_uri(httpretty.GET, rotter_scrapper.resource_url(),
                           body=test_data, content_type='text/html')
    assert_is_instance(rotter_scrapper.scrape_resource(), list)
    rotter_scrapper._titles_count = 10
    assert_equal(len(rotter_scrapper.scrape_resource()), rotter_scrapper.titles_count)
    rotter_scrapper._titles_count = 25
    assert_equal(len(rotter_scrapper.scrape_resource()), rotter_scrapper.titles_count)


@httpretty.activate
@with_setup(create_scrapper_instance)
@with_setup(create_fake_requests_mock_data)
def test_scrape_resource_return_data():
    httpretty.register_uri(httpretty.GET, rotter_scrapper.resource_url(),
                           body=test_data, content_type='text/html')
    for elem in rotter_scrapper.scrape_resource():
        # we can use 'all(...)' but then when a test fails, its less verbose
        assert_true('title' in elem)
        assert_true('url' in elem)
        assert_true('scraped_at' in elem)


# Real tests - do not comment out!
@nottest
def test_real_scrape_resource():
    for r in Rotter(titles_count=50).scrape_resource():
        print(r)


@nottest
def test_real_rotter_call_():
    r = Rotter(titles_count=20)()
    for e in r:
        print(e['title_en'])
