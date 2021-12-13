from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule
import json


bp = Blueprint("Info output")


@bp.on.message(ForEveryoneRule("show_config"), text="<prefix>конфиг")
async def config(message: Message):
    with open("config.json", "r") as f:
        content = json.load(f)
    await edit_msg(
        bp.api,
        message,
        f'Debug: {content["debug"]}\n'
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
