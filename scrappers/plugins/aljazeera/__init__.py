import scrappers
import scrappers.mixins


class ALJazeera(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """AL Jazeera RSS feed (http://www.aljazeera.com/xml/rss/all.xml) scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'cp1252'

    def resource_url(self):
        return 'http://www.aljazeera.com/xml/rss/all.xml'
