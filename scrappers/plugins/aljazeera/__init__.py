import scrappers
import sys
from datetime import datetime
from lxml import etree


class ALJazeera(scrappers.Scrapper):
    """AL Jazeera RSS feed (http://www.aljazeera.com/xml/rss/all.xml) scrapper.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_translate(self):
        return False

    def resource_url(self):
        return 'http://www.aljazeera.com/xml/rss/all.xml'

    def scrape_resource(self):
        scraped_data = list()
        resource_url = self.resource_url()
        parser = etree.XMLParser(strip_cdata=False)
        scrapped_count = 0
        try:
            data = self.get_resource(resource_url)
            root = etree.XML(data.text.encode('cp1252'), parser)
            for item in root.xpath('//channel/item'):
                title = item.xpath('title')[0].text.strip()
                url = item.xpath('link')[0].text.strip()
                scraped_at = datetime.utcnow()
                scraped_data.append({'title': title, 'url': url, 'scraped_at': scraped_at})
                scrapped_count += 1
                if scrapped_count == self.titles_count: break
        except Exception as e:
            print("[ERROR]: Could not properly scrape that data: %s" % str(e), file=sys.stderr)
        finally:
            return scraped_data
