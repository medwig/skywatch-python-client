import os
import json


def read_config_file():
    filename = os.path.join(os.path.expanduser('~'), '.skywatch.json')
    with open(filename, 'r') as f:
        data = json.loads(f.read())

    return data


def get_apikey_from_config():
    config = read_config_file()
    return config['api_key']
