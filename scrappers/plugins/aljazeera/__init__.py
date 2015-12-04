import scrappers
import scrappers.mixins


class ALJazeera(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """AL Jazeera RSS feed scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'utf-8'

    def resource_urls(self):
        return [{'category': 'All News', 'url': 'http://www.aljazeera.com/xml/rss/all.xml'}]
