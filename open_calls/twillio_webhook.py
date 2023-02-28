import yaml
from os.path import exists
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger
from character import player

import json 
import pickle


yml_configs = {}
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)


def handle_request():
    logger.debug(request.form)
    act = None
    if exists( f"users/{request.form['From']}.pkl") :
        with open(f"users/{request.form['From']}.pkl", 'rb') as p:
            act = pickle.load(p)
            logger.debug("user exists")
            output = act.get_output(request.form['Body']) 
            #print(output) debug
        for o_msg in output:
            logger.debug("returned from the character function")
            message = g.sms_client.messages.create(
                     body=o_msg,
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])

    else:
        act = player(request.form['From'],0,100)
        logger.debug("user doesnt exists creating player")
        om_menu = act.get_mm()
        #print(om_menu) debug
        message = g.sms_client.messages.create(
                     body=om_menu,
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])

    with open(f"users/{request.form['From']}.pkl", 'wb') as p:
        pickle.dump(act, p)
    return json_response( sid = message.sid )
