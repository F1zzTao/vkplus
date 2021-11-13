from vkwave.bots import (
    SimpleLongPollUserBot,
)
from json import loads
from commands.settings import settings_router
from commands.blank import blank_router
from commands.bomb import bomb_router
from commands.demotivator import demotivator_router
from commands.info import info_router
from commands.settings import settings_router
from commands.interactive_commands import interactive_router
from commands.random_case import random_router
from commands.advancements import advancements_router
from commands.show_config import config_router
from middlewares.is_me_middleware import FromMeMiddleware

defaultConfig = """{
    "token": "",
    "user_id": "",
    "prefix": "!",
    "work_for_everyone": false,
    "delete_after": 5,
    "bomb_time": 10,
    "send_info_in_dm": true,
    "edit_or_delete": "edit"
}"""

try:
    with open('config.json', 'r') as f:
        content = loads(f.read())
except FileNotFoundError:
    print("Конфиг не найден, я его создам, а вы заполните его...")
    with open('config.json', 'w') as f:
        f.write(defaultConfig)
        raise FileNotFoundError("Config not found")

bot = SimpleLongPollUserBot(tokens=content["token"])
bot.middleware_manager.add_middleware(FromMeMiddleware())
bot.dispatcher.add_router(settings_router)
bot.dispatcher.add_router(blank_router)
bot.dispatcher.add_router(bomb_router)
bot.dispatcher.add_router(demotivator_router)
bot.dispatcher.add_router(info_router)
bot.dispatcher.add_router(interactive_router)
bot.dispatcher.add_router(random_router)
bot.dispatcher.add_router(advancements_router)
bot.dispatcher.add_router(config_router)

bot.run_forever()
