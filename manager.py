"""
Project execution / entry point for all parts:
1) Scrappers
2) Workers
3) Server (HTTP)
"""
from flask.ext.script import Manager, Server
from scrappers.commands import Scrapper
from server import server_app
import log

manager = Manager(server_app)

manager.add_command('runserver', Server(host=server_app.config['SERVER_HOST'], port=server_app.config['SERVER_PORT']))
manager.add_command('scrapper',
                    Scrapper(redis_host=server_app.config['REDIS_HOST'], redis_port=server_app.config['REDIS_PORT']))

if __name__ == "__main__":
    manager.run()
