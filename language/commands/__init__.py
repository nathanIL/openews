from flask.ext.script import Command, Option, Group
from rq import Queue
from redis import Redis
from server.db import MongoClientContext


class Language(Command):
    """
    Manage Natural Language Processing (NLP) related tasks.
    """

    def __init__(self, redis_conn_rec, mongo_conn_rec, raw_mongo_db_name, jobs_queue):
        super().__init__()
        self._jobs_queue = jobs_queue
        self._mongo_conn_red = mongo_conn_rec
        self._raw_mongo_db_name = raw_mongo_db_name
        self._queue = Queue(self.jobs_queue_name, connection=Redis(**redis_conn_rec._asdict()))

    @property
    def jobs_queue_name(self):
        return self._jobs_queue

    def get_options(self):
        return [Group(Option('--stats', dest='stats', action='store_true',
                             help='Shows documents statistics (bundled, categorized, etc'),
                      exclusive=True,
                      required=True)]

    def run(self, **options):
        if options['stats']:
            # TODO: Implement
            with MongoClientContext(self._mongo_conn_red) as mc:
                scrapped_db = mc[self._raw_mongo_db_name]
                print("Listing `")
                for collection in scrapped_db.collection_names(include_system_collections=False):
                    total_documents_count = scrapped_db[collection].count()
                    bundled_documents_count = scrapped_db[collection].find({'bundled': {'$exists': True}}).count()
                    print("""
=======================================
{0}
{1}
 * Total Documents: {2}
 * Bundled: {3}
=======================================
                    """.format(collection, '-' * len(collection),
                               total_documents_count,
                               bundled_documents_count))
                    # print(" {0}: {1}/{2} (Total Documents / Bundled Documents)".format(collection,
                    #                                                                    total_documents_count,
                    #                                                                    bundled_documents_count))
