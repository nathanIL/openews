from flask.ext.script import Command, Option, Group
from rq import Queue
from redis import Redis


class Language(Command):
    """
    Manage Natural Language Processing (NLP) related tasks.
    """

    def __init__(self, redis_host, redis_port, jobs_queue):
        super().__init__()
        self._jobs_queue = jobs_queue
        redis = Redis(host=redis_host, port=redis_port)
        self._queue = Queue(self.jobs_queue_name, connection=redis)

    @property
    def jobs_queue_name(self):
        return self._jobs_queue

    def get_options(self):
        return [Group(Option('--status', dest='sim_status', action='store_true',
                             help='Shows similarity status between scrapped documents'),
                      exclusive=True,
                      required=True)]

    def run(self, **options):
        if options['sim_status']:
            pass
