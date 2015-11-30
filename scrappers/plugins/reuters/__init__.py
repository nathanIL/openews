import scrappers
import scrappers.mixins


class Reuters(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """Reuters RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'utf-8'

    def resource_urls(self):
        return [{'category': 'Top News', 'url': 'http://feeds.reuters.com/reuters/topNews?format=xml'},
                {'category': 'US News', 'url': 'http://feeds.reuters.com/Reuters/domesticNews?format=xml'},
                {'category': 'Word News', 'url': 'http://feeds.reuters.com/Reuters/worldNews?format=xml'},
                {'category': 'Politics', 'url': 'http://feeds.reuters.com/Reuters/PoliticsNews?format=xml'}]
