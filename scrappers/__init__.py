"""
A Scrapper instance is an entity that collects data from the resources.
"""
import abc
import requests


class Scrapper(metaclass=abc.ABCMeta):
    """
    Scrappers Abstract Base Class.
    All scrappers must inherit and implement required methods, etc.
    """

    def __init__(self, titles_count=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._titles_count = titles_count

    @property
    def titles_count(self):
        """
        We refer to "title" as an atomic sentence to be retrieved.
        For instance, a forum thread subject.
        :return: The max number (int) of titles to scrape from the source.
        """
        return self._titles_count

    @abc.abstractproperty
    def resource_url(self):
        """
        Must be implemented by inheriting class and return the base (parent) source from which we start to scrape.
        :return: string holding a valid URL to start scraping from.
        """
        pass

    @abc.abstractmethod
    def scrape_resource(self):
        """
        Scrapes the provided resource up to titles_count.
        :return: a list holding the scraped titles as dict values (title, url) as keys
        """
        pass

    def get_resource(self, resource):
        return requests.get(resource, verify=False)
