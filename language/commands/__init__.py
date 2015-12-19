from flask.ext.script import Command, Option, Group
from rq import Queue
from redis import Redis
from language.utils import stats
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

    @staticmethod
    def get_options():
        return [Group(Option('--raw_stats', dest='raw_stats', action='store_true',
                             help='Shows raw database scrapper statistics'),
                      exclusive=True,
                      required=True)]

    def run(self, **options):
        if options['raw_stats']:
            with MongoClientContext(self._mongo_conn_red) as mc:
                statistics = stats(mc)
                if statistics:
                    print("Listing raw database scrapped documents statistics:")
                    for col in statistics:
                        print("""
=======================================
{0}
{1}
 * Total Documents: {2}
 * Bundled: {3}
 * Last scrapped at: {4}
=======================================
                    """.format(col.title(), '-' * len(col),
                               statistics.get(col)['documents_count'],
                               statistics.get(col)['bundled'],
                               statistics.get(col)['last_scrapped_at']))
