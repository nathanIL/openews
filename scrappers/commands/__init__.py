from flask.ext.script import Command, Option, Group
from scrappers.utils import scrapper_classes
from rq import Queue
from redis import Redis
import subprocess
import sys
import warnings


class Scrapper(Command):
    """
    Manage scrappers (workers, jobs) related tasks.
    """

    def __init__(self, redis_host, redis_port, jobs_queue):
        super().__init__()
        self._jobs_queue = jobs_queue
        redis = Redis(host=redis_host, port=redis_port)
        self._scrappers = {s.__name__: s for s in scrapper_classes() if not s.disabled()}
        self._queue = Queue(self.jobs_queue_name, connection=redis)

    @property
    def jobs_queue_name(self):
        return self._jobs_queue

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
            print(" Queuing to redis job queue: %s\n" % self.jobs_queue_name)
            print("\t * Queueing: %s" % options['queue_scrapper'])
            job = self._queue.enqueue(self._scrappers.get(options['queue_scrapper'])(), result_ttl=300)
            print("\t   Queued Job ID: %s" % job.get_id())
        elif options['queue_all']:
            print(" Queuing to redis job queue: %s\n" % self.jobs_queue_name)
            for scrapper in self._scrappers.values():
                print("\t * Queueing: %s" % scrapper.__name__)
                job = self._queue.enqueue(scrapper(), result_ttl=300)
                print("\t   Queued Job ID: %s" % job.get_id())
        elif options['run_worker']:
            # Some issues with directly using rq.Worker, rq.Queue and rq.Connection, so for now calling
            # rqworker directly.
            try:
                process_output = subprocess.check_call(['rqworker', '--burst', self.jobs_queue_name])
                print(process_output)
            except KeyboardInterrupt:
                pass
            except subprocess.CalledProcessError as e:
                warnings.warn(e.output)
                sys.exit(e.returncode)


