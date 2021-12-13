from vkbottle import User, load_blueprints_from_package
from middlewares.is_me_middleware import FromMeMiddleware

import json
from time import time

import logging


defaultConfig = """{
    "token": "",
    "debug": false,
    "user_id": "",
    "prefix": "!",
    "delete_after": 5,
    "bomb_time": 10,
    "send_info_in_dm": true,
    "edit_or_send": "edit",
}"""

with open("config.json", "r") as f:
    content = json.load(f)

FORMAT = "%(message)s"
logging.basicConfig(
    level=("DEBUG" if content["debug"] is True else "INFO")
)

bot = User(content["token"])
for bp in load_blueprints_from_package("commands"):
    bp.load(bot)
bot.labeler.message_view.register_middleware(FromMeMiddleware)

with open("time_started.txt", "w") as f:
    f.write(str(round(time())))

bot.run_forever()
