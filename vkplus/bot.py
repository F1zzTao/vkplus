"""
VK+ by Timur Bogdanov (timius100)

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

More information: https://github.com/timius100/vkplus
"""
import json
import logging
from time import time
from os import mkdir
from os.path import exists
from middlewares.has_prefix_middleware import HasPrefixMiddleware
from vkbottle import User, load_blueprints_from_package


if __name__ == "__main__":
    if not exists('output'):
        mkdir('output')

    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)

    logging.basicConfig(
        level=("DEBUG" if content["debug"] is True else "INFO")
    )

    bot = User(content["token"])
    for bp in load_blueprints_from_package("commands"):
        bp.load(bot)
    bot.labeler.message_view.register_middleware(HasPrefixMiddleware)

    with open("time_started.txt", "w", encoding="utf-8") as file:
        file.write(str(round(time())))

    bot.run_forever()
