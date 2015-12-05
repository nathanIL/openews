"""
All logging related stuff for the project will go here.
"""
import logging
import logging.config
import json
from manager import server_app

config_dict = json.loads(''.join(open(server_app.config['LOG_CONFIG']).readlines()))
logging.config.dictConfig(config_dict)
