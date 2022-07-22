"""
Help message, that includes all the commands
"""
from vkbottle.user import Blueprint, Message
import json

from utils.edit_msg import edit_msg
from utils.emojis import ENABLED
from filters import ForEveryoneRule


bp = Blueprint("help command")


@bp.on.message(
    ForEveryoneRule("help"), text=["<prefix>помощь", "<prefix>help"]
)
async def help_handler(message: Message):
    with open("commands_settings.json", "r", encoding="utf-8") as file:
        commands_info = json.load(file)

    info = "Список команд:\n"
    for command in commands_info.items():
        for description in command[1]["description"]:
            info += description + "\n"
    info += "\nБольше информации: https://github.com/timius100/vkplus"

    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    await bp.api.messages.send(
        peer_id=config["user_id"], message=info, random_id=0
    )
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{ENABLED} | Информация о всех командах отправлена в личные "
            "сообщения!"
        ),
    )
