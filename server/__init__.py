import os
from flask import Flask
from flask.ext.pymongo import PyMongo

server_app = Flask(__name__)
if 'OPENEWS_DEVELOPMENT_ENV' in os.environ:
    server_app.config.from_object('config-development')
else:
    server_app.config.from_object('config-production')
mongo = PyMongo(server_app)