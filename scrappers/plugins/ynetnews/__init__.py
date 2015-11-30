import scrappers
import scrappers.mixins


class YnetNews(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """Ynet English news RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'windows-1255'

    def resource_urls(self):
        return [{'category': 'All News', 'url': 'http://www.ynet.co.il/Integration/StoryRss3082.xml'}]
