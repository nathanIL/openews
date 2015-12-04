from flask.ext.script import Command, Option, Group
from scrappers.utils import scrapper_classes
from rq import Queue
from redis import Redis


class Scrapper(Command):
    """
    Manage scrappers and scrapper's worker.
    """

    def __init__(self, redis_host, redis_port):
        super().__init__()
        redis = Redis(host=redis_host, port=redis_port)
        self._scrappers = { s.__name__: s for s in scrapper_classes()}
        self._queue = Queue(connection=redis)

    def get_options(self):
        return [Group(Option('--list', dest='list_scrappers', action='store_true', help='List available scrappers'),
                      Option('--queue_scrapper', dest='queue_scrapper', type=str,
                             choices=[s for s in self._scrappers.keys()],
                             help='Queue a single scrapper (see --list for supported scrappers)'),
                      Option('--queue_all', dest='queue_all', action='store_true',
                             help='Queue all available scrappers (see --list for supported scrappers)'),
                      Option('--run_worker', dest='run_worker',
                             help='Run a single worker to process queued scrappers', action='store_true'),
                      exclusive=True,
                      required=True)]

    def run(self, **options):
        if options['list_scrappers']:
            print("Available scrappers:")
            for i, s in enumerate(self._scrappers.values(), start=1):
                print("\t%d - %s: %s" % (i, s.__name__, s.__doc__.splitlines()[0]))
        elif options['queue_scrapper']:
            self._queue.enqueue(self._scrappers.get(options['queue_scrapper'])())
        elif options['queue_all']:
            for scrapper in self._scrappers.values():
                self._queue.enqueue(scrapper())
        elif options['run_worker']:
            pass
