import scrappers
import scrappers.mixins
import re


class Telegraph(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """Telegraph RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'utf-8'

    def skipping_rules(self, title):
        """ Skip some non relevant news titles that we want to skip, like Pictures of the day, etc.
        :param title: The scraped title
        :return: True if we want to skip, otherwise False.
        """
        skip_regexs = [re.compile(r'^\s*Pictures\s+of\s+the\s+day:', re.IGNORECASE)]
        return any([r.match(title) for r in skip_regexs])

    def resource_urls(self):
        # TODO: Telegraph has hunderends of iteresting RSS feeds. we can scrape all of them and create the return list
        # based on this scrape.This probably applies to many other RSS sources.
        return [{'category': 'UK News', 'url': 'http://www.telegraph.co.uk/news/uknews/rss'},
                {'category': 'Israel', 'url': 'http://www.telegraph.co.uk/news/worldnews/middleeast/israel/rss'},
                {'category': 'Word News', 'url': 'http://www.telegraph.co.uk/news/worldnews/rss'},
                {'category': 'Politics', 'url': 'http://www.telegraph.co.uk/news/politics/rss'},
                {'category': 'Islamic State (ISIL)',
                 'url': 'http://www.telegraph.co.uk/news/worldnews/islamic-state/rss'}]
