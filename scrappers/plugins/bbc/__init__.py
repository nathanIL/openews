import scrappers
import re
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

    def skipping_rules(self, title):
        """ BBC has some non relevant news titles that we want to skip, like country profiles, etc.
        :param title: The scraped title
        :return: True if we want to skip, otherwise False.
        """
        skip_regexs = [re.compile(r'.+profile$', re.IGNORECASE),
                       re.compile(r'^(?:\w+(?:\s+|-+)?\w*)\s+profile$', re.IGNORECASE),
                       re.compile(r'.+profile\s*-\s*Overview$', re.IGNORECASE),
                       re.compile(r'^\s*Country\s+profile:.+', re.IGNORECASE),
                       re.compile(r'^\s*(?:In|Your)\s+pictures:', re.IGNORECASE),
                       re.compile(r'^\s*Regions\s+and\s+territories:', re.IGNORECASE),
                       re.compile(r'^VIDEO\s*:.+', re.IGNORECASE)]
        return any([r.match(title) for r in skip_regexs])

    def resource_urls(self):
        return [{'category': 'Middle East', 'url': 'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml'},
                {'category': 'Asia', 'url': 'http://feeds.bbci.co.uk/news/world/asia/rss.xml'},
                {'category': 'US & Canada', 'url': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml'},
                {'category': 'Africa', 'url': 'http://feeds.bbci.co.uk/news/world/africa/rss.xml'},
                {'category': 'Europe', 'url': 'http://feeds.bbci.co.uk/news/world/europe/rss.xml'},
                {'category': 'Latin America', 'url': 'http://feeds.bbci.co.uk/news/world/latin_america/rss.xml'},
                {'category': 'Top Stories', 'url': 'http://feeds.bbci.co.uk/news/rss.xml'},
                {'category': 'World', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml'},
                {'category': 'Politics', 'url': 'http://feeds.bbci.co.uk/news/politics/rss.xml'}]
