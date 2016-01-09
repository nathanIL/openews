import scrappers
import scrappers.mixins


class FoxNews(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """The Fox News RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'UTF-8'

    def resource_urls(self):
        return [{'category': 'World', 'url': 'http://feeds.foxnews.com/foxnews/world'},
                {'category': 'US', 'url': 'http://feeds.foxnews.com/foxnews/national'},
                {'category': 'Tech', 'url': 'http://feeds.foxnews.com/foxnews/tech'},
                {'category': 'Science', 'url': 'http://feeds.foxnews.com/foxnews/science'},
                {'category': 'Most Popular', 'url': 'http://feeds.foxnews.com/foxnews/most-popular'},
                {'category': 'Latest', 'url': 'http://feeds.foxnews.com/foxnews/latest'}]
