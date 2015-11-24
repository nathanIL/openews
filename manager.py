"""
Project execution / entry point for all parts:
1) Scrappers
2) Workers
3) Server (HTTP)
"""
from flask.ext.script import Manager, Server

from scrappers.commands import Scrapper
from server import server_app

manager = Manager(server_app)


manager.add_command('runserver', Server(host="0.0.0.0", port=9000))
manager.add_command('scrapper',  Scrapper())

if __name__ == "__main__":
    manager.run()