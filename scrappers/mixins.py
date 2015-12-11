from datetime import datetime
from lxml import etree


class RSSScrapper(object):
    """
    Mixin for RSS based resources. most (or all?) have the same structure.
    This mixin requires the inheriting class to also inherit from scrappers.Scrapper ABC.
    """

    def scrape_resources(self):
        scraped_data = {'categories': []}
        resource_urls = self.resource_urls()
        parser = etree.XMLParser(strip_cdata=False, recover=True)
        scrapped_count = 0
        try:
            for data in self.get_resources(resource_urls):
                self.logger().debug("Scrapping data from resource: %s", data)
                # TODO: should we really use 'replace' here?
                root = etree.XML(data['data'].text.encode(self.encoding(), errors='replace'), parser)
                for item in root.xpath('//channel/item'):
                    title = item.xpath('title')[0].text.strip()
                    if self.skip_scrape(title):
                        self.logger().debug("Skipping this title {0} resource due to a predefined scrapper rule".format(title))
                        continue
                    url = item.xpath('link')[0].text.strip()
                    scraped_at = datetime.utcnow()
                    scraped_data['categories'].append({'category': data['category'], 'title': title, 'url': url, 'scraped_at': scraped_at})
                    scrapped_count += 1
                    if scrapped_count and scrapped_count == self.titles_count:
                        break
                if scrapped_count and scrapped_count == self.titles_count:
                    break
        except Exception as e:
            self.logger().exception("Could not properly scrape resources")
        finally:
            return scraped_data
