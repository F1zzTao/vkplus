from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from json import loads
from os import getcwd

bp = Blueprint("Info output")
config_path = getcwd().replace("\\", "/") + "/config.json"


@bp.on.message(text="<prefix>конфиг")
async def config(message: Message):
    with open(config_path, "r") as f:
        content = loads(f.read())
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        "Токен: _______________\n"
        f'Айди: {content["user_id"]}\n'
        f'Префикс: {content["prefix"]}\n'
        f'Для всех: {"да" if content["work_for_everyone"] else "нет"}\n'
        "Удалять после: "
        f'{"не удалять" if content["delete_after"] == 0 else str(content["delete_after"]) + " секунд"}\n'  # noqa: E501
        f'Время бомбы: {content["bomb_time"]} секунд\n'
        "Информация о человеке в лс: "
        f'{"да" if content["send_info_in_dm"] else "нет"}\n'
        "Редактировать, или отправлять: "
        f'{"редактировать" if content["edit_or_send"] == "edit" else "отправлять"}',  # noqa: E501
    )
