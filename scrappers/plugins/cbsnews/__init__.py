import scrappers
import re
import scrappers.mixins


class CBSNews(scrappers.mixins.RSSScrapper, scrappers.Scrapper):
    """The CBS News RSS feeds scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def encoding(self):
        return 'UTF-8'

    def skipping_rules(self, title):
        """
        :param title: The scraped title
        :return: True if we want to skip, otherwise False.
        """
        skip_regexs = [re.compile(r'^Photos\s+of\s+the\s+week', re.IGNORECASE)]
        return any([r.match(title) for r in skip_regexs])

    def resource_urls(self):
        return [{'category': 'Top Stories', 'url': 'http://www.cbsnews.com/latest/rss/main'},
                {'category': 'US', 'url': 'http://www.cbsnews.com/latest/rss/us'},
                {'category': 'Sci-Tech', 'url': 'http://www.cbsnews.com/latest/rss/tech'},
                {'category': 'World', 'url': 'http://www.cbsnews.com/latest/rss/world'},
                {'category': 'Politics', 'url': 'http://www.cbsnews.com/latest/rss/politics'}]
