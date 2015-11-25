from nose.tools import assert_is_instance, assert_true
from scrappers.plugins.rotter import Rotter
import validators

def test_instance_creation():
    assert_is_instance(Rotter(), Rotter)

def test_resource_url():
    assert_true(validators.url(Rotter().resource_url()))