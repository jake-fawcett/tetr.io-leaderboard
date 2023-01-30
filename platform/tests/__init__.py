import json
import os


def load_configuration(cls):
    config_json = os.environ.get('DEPLOYOUTPUT')
    if config_json is None:
        with open('config.json', 'r') as f:
            config_json = f.read()
    if config_json is None:
        raise Exception('Unable to load configuration')
    return json.loads(config_json)
