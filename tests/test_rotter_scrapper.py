from nose.tools import nottest, with_setup, assert_is_instance, assert_true, assert_equal
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


@nottest
def test_real_scrape_resource():
    """
    For real test only
    """
    for r in Rotter(titles_count=50).scrape_resource():
        print(r)
