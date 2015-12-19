import pymongo
from collections import defaultdict
from server import server_app


def stats(mc, raw_db_name=server_app.config['MONGO_RAW_COLLECTION']):
    """
    Return raw database statistics.
    :param mc: server.db.MongoClientContext instance
    :param raw_db_name: the raw mongo database name
    :return: a dict. key is the scrapper, values are dicts of stats
    """
    results = defaultdict(dict)
    scrapped_db = mc[raw_db_name]
    for collection in scrapped_db.collection_names(include_system_collections=False):
        total_documents_count = scrapped_db[collection].count()
        bundled_documents_count = scrapped_db[collection].find({'bundled': {'$exists': True}}).count()
        results[collection]['documents_count'] = total_documents_count
        results[collection]['bundled'] = bundled_documents_count
        results[collection]['last_scrapped_at'] = scrapped_db[collection].find().sort('scraped_at',
                                                                                      pymongo.DESCENDING)[0]['scraped_at']

    return results
