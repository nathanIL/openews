"""
Project execution / entry point for all parts:
1) Scrappers
2) Workers
3) Server (HTTP)
4) NLP
"""
from flask.ext.script import Manager, Server
from scrappers.commands import Scrapper
from language.commands import Language
from server import server_app
from server.db import MongoConnectionRecord, RedisConnectionRecord
import log

manager = Manager(server_app)
mongo_connection_record = MongoConnectionRecord(host=server_app.config['MONGO_HOST'],
                                                port=server_app.config['MONGO_PORT'],
                                                connect=False)
redis_connection_record = RedisConnectionRecord(host=server_app.config['REDIS_HOST'],
                                                port=server_app.config['REDIS_PORT'])

manager.add_command('runserver', Server(host=server_app.config['SERVER_HOST'], port=server_app.config['SERVER_PORT']))
manager.add_command('scrapper',
                    Scrapper(redis_conn_rec=redis_connection_record,
                             jobs_queue=server_app.config['SCRAPPERS_JOBS_QUEUE']))

manager.add_command('language',
                    Language(redis_conn_rec=redis_connection_record,
                             mongo_conn_rec=mongo_connection_record,
                             raw_mongo_db_name=server_app.config['MONGO_SCRAPPERS_DB'],
                             jobs_queue=server_app.config['NLP_PROCESS_QUEUE']))

if __name__ == "__main__":
    manager.run()
