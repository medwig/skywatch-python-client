import os
import json

IOError_message = '''An API-key must be set. Two options:
    1. Pass api key to the api client: skywatch.Client('your-api-key')
    2. Create a key file ~/.skywatch.json with the format:
{
    "api_key": "your-api-key"
}'''

KeyError_message = '''Cannot find "api_key" in ~/.skywatch.json. Are you sure it is in valid JSON format? Example:
\t\t{
    "api_key": "your-api-key"
}'''

def _read_config_file():
    filename = os.path.join(os.path.expanduser('~'), '.skywatch.json')
    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    except IOError:
        raise IOError(IOError_message)
    return data


def get_api_key():
    config = _read_config_file()
    try:
        api_key = config['api_key']
    except KeyError:
        raise IOError(KeyError_message)
    return api_key
