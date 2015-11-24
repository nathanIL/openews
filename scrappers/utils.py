import os
import sys


def scrapper_classes():
    """
    Finds all available scrappers and returns a list with their class objects.
    :return: list of scrapper classes
    """
    import importlib
    import inspect

    classes = []
    scrappers_parent_dir = os.path.dirname(os.path.realpath(__file__))
    for scrapper in [e for e in os.listdir(scrappers_parent_dir) if
                     os.path.isdir(os.path.join(scrappers_parent_dir, e)) and not e.startswith('_')]:
        module = importlib.import_module('scrappers.%s' % scrapper)
        classes.extend([obj for name, obj in inspect.getmembers(module) if inspect.isclass(obj)])

    return classes
