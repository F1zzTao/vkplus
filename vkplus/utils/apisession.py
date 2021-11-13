from vkwave.bots import create_api_session_aiohttp
from json import loads
from os import getcwd

config_path = getcwd().replace('\\', '/')+'/config.json'

with open(config_path, 'r') as f:
    config = loads(f.read())

api_session = create_api_session_aiohttp(config['token']).api.get_context()
