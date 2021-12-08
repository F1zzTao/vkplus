from vkbottle import User, load_blueprints_from_package
from json import loads

from middlewares.is_me_middleware import FromMeMiddleware

import logging
from rich.logging import RichHandler

defaultConfig = """{
    "token": "",
    "debug": false,
    "user_id": "",
    "prefix": "!",
    "work_for_everyone": false,
    "delete_after": 5,
    "bomb_time": 10,
    "send_info_in_dm": true,
    "edit_or_send": "edit"
}"""

try:
    with open("config.json", "r") as f:
        content = loads(f.read())
except FileNotFoundError:
    print("Конфиг не найден, я его создам, а вы заполните его...")
    with open("config.json", "w") as f:
        f.write(defaultConfig)
        raise FileNotFoundError("Config not found")

FORMAT = "%(message)s"
logging.basicConfig(
    level=("DEBUG" if content["debug"] is True else "INFO"),
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()],
)

log = logging.getLogger("rich")

bot = User(content["token"])
for bp in load_blueprints_from_package("commands"):
    bp.load(bot)
bot.labeler.message_view.register_middleware(FromMeMiddleware)

bot.run_forever()
