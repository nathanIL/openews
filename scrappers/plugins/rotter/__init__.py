import scrappers
import sys
import re
from bs4 import BeautifulSoup


class Rotter(scrappers.Scrapper):
    """Rotter forum (http://rotter.net/scoopscache.html) scrapper.
    From side experiment, we can do something similar to:
    gs = goslate.Goslate()
    for file in [ join('pages',f) for f in listdir('pages') if isfile(join('pages',f)) ]:
    posts = BeautifulSoup(open(file), "html.parser").find_all('font', attrs={"class": "text15bn"})
    for p in posts:
        text = p.find('b').text
        #translated = gs.translate(text, 'en')
        print(text)
        #print(translated)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resource_url(self):
        return 'http://rotter.net/cgi-bin/forum/dcboard.cgi?az=list&forum=scoops1&mm=1&archive='

    def scrape_resource(self):
        scraped_data = list()
        resource_url = self.resource_url()
        page = 2
        try:
            while len(scraped_data) < self.titles_count:
                data = self.get_resource(resource_url)
                if not data:
                    break
                data.encoding = 'cp1255'  # For hebrew
                posts = BeautifulSoup(data.text, "html.parser").find_all('font', attrs={"class": "text15bn"})
                if not posts:
                    break
                how_many = self.titles_count - len(scraped_data)
                scraped_data.extend({('title', p.find('b').text), ('url', p.find('a')['href'])} for p in posts[:how_many])
                resource_url = re.sub(r'&mm=\d+', '&mm=%d' % page, resource_url)
                page += 1
        except Exception as e:
            print("[ERROR]: Could not properly scrape that data: %s" % str(e), file=sys.stderr)
        finally:
            return scraped_data
