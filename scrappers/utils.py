def scrapper_classes():
    """
    Finds all available scrappers and returns a list with their class objects.
    :return: list of scrapper classes
    """
    from scrappers import Scrapper
    import importlib
    import inspect
    import logging
    import os

    classes = []
    logger = logging.getLogger('openews.scrappers')
    scrappers_parent_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plugins')
    for scrapper in [e for e in os.listdir(scrappers_parent_dir) if
                     os.path.isdir(os.path.join(scrappers_parent_dir, e)) and not e.startswith('_')]:
        module = importlib.import_module('scrappers.plugins.%s' % scrapper)
        logger.debug('Loading module: %s', module)
        classes.extend(
            [obj for name, obj in inspect.getmembers(module) if inspect.isclass(obj) and issubclass(obj, Scrapper)])

    return classes
