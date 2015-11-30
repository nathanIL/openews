import scrappers
import scrappers.mixins


class BBC(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """BBC RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'utf-8'

    def resource_urls(self):
        return [{'category': 'Middle East', 'url': 'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml'},
                {'category': 'Asia', 'url': 'http://feeds.bbci.co.uk/news/world/asia/rss.xml'},
                {'category': 'US & Canada', 'url': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml'},
                {'category': 'Africa', 'url': 'http://feeds.bbci.co.uk/news/world/africa/rss.xml'},
                {'category': 'Europe', 'url': 'http://feeds.bbci.co.uk/news/world/europe/rss.xml'},
                {'category': 'Latin America', 'url': 'http://feeds.bbci.co.uk/news/world/latin_america/rss.xml'},
                {'cateogry': 'Top Stories', 'url': 'http://feeds.bbci.co.uk/news/rss.xml'},
                {'cateogry': 'World', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml'},
                {'cateogry': 'Politics', 'url': 'http://feeds.bbci.co.uk/news/politics/rss.xml'}]
