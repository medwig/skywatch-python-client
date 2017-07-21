import os
import json


def _read_config_file():
    filename = os.path.join(os.path.expanduser('~'), '.skywatch.json')
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    return data


def get_api_key():
    config = _read_config_file()
    api_key = config['api_key']
    return api_key
