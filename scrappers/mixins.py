from datetime import datetime
from lxml import etree
import sys


class RSSScrapper(object):
    """
    Mixin for RSS based resources. most (or all?) have the same structure.
    """
    def scrape_resource(self):
        scraped_data = list()
        resource_url = self.resource_url()
        parser = etree.XMLParser(strip_cdata=False)
        scrapped_count = 0
        try:
            data = self.get_resource(resource_url)
            root = etree.XML(data.text.encode(self.encoding()), parser)
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
