from flask.ext.script import Command, Option, Group
from rq import Queue
from redis import Redis
from language.utils import stats


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
        return [Group(Option('--stats', dest='stats', action='store_true',
                             help='Shows documents statistics (bundled, total, etc'),
                      exclusive=True,
                      required=True)]

    def run(self, **options):
        if options['stats']:
            statistics = stats(self._mongo_conn_red, self._raw_mongo_db_name)
            if statistics:
                print("Listing scrapped documents statistics:")
                for col in statistics:
                    print("""
=======================================
{0}
{1}
 * Total Documents: {2}
 * Bundled: {3}
=======================================
                    """.format(col.title(), '-' * len(col),
                               statistics.get(col)['documents_count'],
                               statistics.get(col)['bundled']))
