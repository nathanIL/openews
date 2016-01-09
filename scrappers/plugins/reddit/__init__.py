import scrappers
import scrappers.mixins


class Reddit(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """The Reddit RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'UTF-8'

    def resource_urls(self):
        return [{'category': 'Front Page', 'url': 'https://www.reddit.com/.rss'}]
