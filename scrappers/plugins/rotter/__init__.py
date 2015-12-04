import scrappers
import sys
import re
from datetime import datetime
from bs4 import BeautifulSoup


class Rotter(scrappers.Scrapper):
    """Rotter forum (http://rotter.net/scoopscache.html) scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def disabled():
        return True

    def should_translate(self):
        """
        Hebrew posts by majority.
        :return: True
        """
        return True

    def resource_urls(self):
        return ['http://rotter.net/cgi-bin/forum/dcboard.cgi?az=list&forum=scoops1&mm=1&archive=']

    def encoding(self):
        """
        cp1252 for hebrew
        :return:
        """
        return 'cp1252'

    def scrape_resource(self):
        scraped_data = list()
        resource_url = self.resource_urls().pop()
        page = 2
        try:
            while len(scraped_data) < self.titles_count:
                data = self.get_resources(resource_url)[0]
                if not data:
                    break
                data.encoding = self.encoding
                posts = BeautifulSoup(data.text, "html.parser").find_all('font', attrs={"class": "text15bn"})
                if not posts:
                    break
                how_many = self.titles_count - len(scraped_data)
                scraped_data.extend(
                    {'title': p.find('b').text, 'url': p.find('a')['href'], 'scraped_at': datetime.utcnow()} for p in
                    posts[:how_many])
                resource_url = re.sub(r'&mm=\d+', '&mm=%d' % page, resource_url)
                page += 1
        except Exception as e:
            print("[ERROR]: Could not properly scrape that data: %s" % str(e), file=sys.stderr)
        finally:
            return scraped_data
