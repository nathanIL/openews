import scrappers
import scrappers.mixins


class NYTimes(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """The New York Times RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'UTF-8'

    def resource_urls(self):
        return [{'category': 'Home', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'},
                {'category': 'Home (Int.)', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/InternationalHome.xml'},
                {'category': 'World', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml'},
                {'category': 'Europe', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml'},
                {'category': 'Middle East', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml'},
                {'category': 'US', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/US.xml'},
                {'category': 'US Politics', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'}]
