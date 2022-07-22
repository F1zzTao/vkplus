"""
Эта команда показывает значения из config.json
"""
import json
from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule


bp = Blueprint("Info output")


@bp.on.message(ForEveryoneRule("show_config"), text="<prefix>конфиг")
async def config(message: Message):
    """
    > !конфиг

    > Айди: 322615766
    > Debug: False
    > Префикс: !
    > Удалять после: 10 секунд
    > Время бомбы: 10 секунд
    > Информация о человеке в лс: да
    > Редактировать, или отправлять: редактировать
    """
    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)
    await edit_msg(
        bp.api,
        message,
        f'Айди: {content["user_id"]}\n'
        f'Debug: {content["debug"]}\n'
        f'Префикс: {content["prefix"]}\n'
        "Удалять после: "
        f'{"не удалять" if content["delete_after"] == 0 else str(content["delete_after"]) + " секунд"}\n'  # noqa: E501
        f'Время бомбы: {content["bomb_time"]} секунд\n'
        "Информация о человеке в лс: "
        f'{"да" if content["send_info_in_dm"] else "нет"}\n'
        "Редактировать, или отправлять: "
        f'{"редактировать" if content["edit_or_send"] == "edit" else "отправлять"}'
    )
