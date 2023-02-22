import yaml
from os.path import exists
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger
from libs.player import player

import json 
import pickle
import random


yml_configs = {}
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)

with open('map.json', 'r') as map_file:
    map = json.load(map_file)

def handle_request():
    logger.debug(request.form)
    act = None
    if exists( f"users/{request.form['From']}.pkl") :
        with open(f"users/{request.form['From']}.pkl", 'rb') as p:
            act = pickle.load(p) 
    else:
        act = player(request.form['From'])
    output = act.get_output(request.form['Body'])

    message = g.sms_client.messages.create(
        body=output,
        from_=yml_configs['twillio']['phone_number'], 
        to=request.form['From'])

    with open(f"users/{request.form['From']}.pkl", 'wb') as p:
        pickle.dump(act, p)

    return json_response( sid = message.sid )
