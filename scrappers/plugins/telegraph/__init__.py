import scrappers
import scrappers.mixins


class Telegraph(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """Telegraph RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'utf-8'

    def resource_urls(self):
        # TODO: Telegraph has hunderends of iteresting RSS feeds. we can scrape all of them and create the return list
        # based on this scrape.This probably applies to many other RSS sources.
        return [{'category': 'UK News', 'url': 'http://www.telegraph.co.uk/news/uknews/rss'},
                {'category': 'Israel', 'url': 'http://www.telegraph.co.uk/news/worldnews/middleeast/israel/rss'},
                {'category': 'Word News', 'url': 'http://www.telegraph.co.uk/news/worldnews/rss'},
                {'category': 'Politics', 'url': 'http://www.telegraph.co.uk/news/politics/rss'},
                {'category': 'Islamic State (ISIL)',
                 'url': 'http://www.telegraph.co.uk/news/worldnews/islamic-state/rss'}]
