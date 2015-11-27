from flask import Flask
from flask.ext.pymongo import PyMongo

server_app = Flask(__name__)
server_app.config.from_object('config')
mongo = PyMongo(server_app)