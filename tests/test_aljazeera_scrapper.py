from nose.tools import nottest, with_setup, assert_is_instance, assert_equal, assert_true
from scrappers.plugins.aljazeera import ALJazeera
import os
import validators
import httpretty

scrapper = None
test_data = None


def create_scrapper_instance():
    global scrapper
    scrapper = ALJazeera()


def create_fake_requests_mock_data():
    global test_data
    xml = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'aljazeera1.xml')
    test_data = ''.join(open(xml).readlines())


@with_setup(create_scrapper_instance)
def test_instance_creation():
    assert_is_instance(scrapper, ALJazeera)


@with_setup(create_scrapper_instance)
def test_resource_url():
    assert_true(all([validators.url(u) for u in scrapper.resource_urls()]))


@httpretty.activate
@with_setup(create_scrapper_instance)
@with_setup(create_fake_requests_mock_data)
def test_scrape_resource():
    for resource in scrapper.resource_urls():
        httpretty.register_uri(httpretty.GET, resource,
                               body=test_data, content_type='text/html')
    assert_is_instance(scrapper.scrape_resource(), list)
    scrapper._titles_count = 10
    assert_equal(len(scrapper.scrape_resource()), scrapper.titles_count)
    scrapper._titles_count = 15
    assert_equal(len(scrapper.scrape_resource()), scrapper.titles_count)


@httpretty.activate
@with_setup(create_scrapper_instance)
@with_setup(create_fake_requests_mock_data)
def test_scrape_resource_return_data():
    for resource in scrapper.resource_urls():
        httpretty.register_uri(httpretty.GET, resource,
                               body=test_data, content_type='text/html')
    for elem in scrapper.scrape_resource():
        # we can use 'all(...)' but then when a test fails, its less verbose
        assert_true('title' in elem)
        assert_true('url' in elem)
        assert_true('scraped_at' in elem)


@with_setup(create_scrapper_instance)
def test_scrapper_should_translate():
    assert_is_instance(scrapper.should_translate(), bool)


# Real tests - do not comment out!
@nottest
def test_real_scrape_resource():
    for r in ALJazeera(titles_count=20).scrape_resource():
        print(r)


@nottest
def test_real_aljazeera_call():
    r = ALJazeera(titles_count=20)
    for e in r():
        print(e)

