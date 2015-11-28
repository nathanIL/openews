import scrappers
import scrappers.mixins


class Reuters(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """Reuters RSS feed (http://feeds.reuters.com/Reuters/worldNews?format=xml) scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'utf-8'

    def resource_url(self):
        return 'http://feeds.reuters.com/Reuters/worldNews?format=xml'
