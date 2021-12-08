from vkbottle import API
from json import loads
from os import getcwd

config_path = getcwd().replace('\\', '/')+'/config.json'

with open(config_path, 'r') as f:
    config = loads(f.read())

api_session = API(config['token'])
