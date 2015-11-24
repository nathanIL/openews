from flask.ext.script import Command, Option, Group
from scrappers.utils import scrapper_classes


class Scrapper(Command):
    """
    A command to manage scrappers.
    """
    def __init__(self):
        super().__init__()

    def get_options(self):
        return [Group(Option('--list', dest='list_scrappers', action='store_true'),
                      Option('--queue_scrapper', dest='queue', type=str),
                      Option('--queue_all', dest='queue_all', action='store_true'),
                      Option('--run_worker', dest='run_worker', type=str),
                      exclusive=True,
                      required=True)]

    def run(self, **options):
        if options['list_scrappers']:
            print("Available scrappers:")
            for i, sc in enumerate(scrapper_classes(), start=1):
                print("\t%d - %s: %s" % (i, sc.__name__, sc.__doc__.splitlines()[0]))
        elif options['queue']:
            pass