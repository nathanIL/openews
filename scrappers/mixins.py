from datetime import datetime
from lxml import etree
import sys


class RSSScrapper(object):
    """
    Mixin for RSS based resources. most (or all?) have the same structure.
    """

    def scrape_resources(self):
        scraped_data = {'categories': []}
        resource_urls = self.resource_urls()
        parser = etree.XMLParser(strip_cdata=False, recover=True)
        scrapped_count = 0
        try:
            for data in self.get_resources(resource_urls):
                # TODO: should we really use 'replace' here?
                root = etree.XML(data['data'].text.encode(self.encoding(), errors='replace'), parser)
                for item in root.xpath('//channel/item'):
                    title = item.xpath('title')[0].text.strip()
                    url = item.xpath('link')[0].text.strip()
                    scraped_at = datetime.utcnow()
                    scraped_data['categories'].append(
                        {'category': data['category'], 'title': title, 'url': url, 'scraped_at': scraped_at})
                    scrapped_count += 1
                    if scrapped_count and scrapped_count == self.titles_count: break
                if scrapped_count and scrapped_count == self.titles_count: break
        except Exception as e:
            print("[ERROR]: Could not properly scrape that data: %s" % str(e), file=sys.stderr)
        finally:
            return scraped_data
