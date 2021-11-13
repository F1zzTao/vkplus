from vkwave.bots import (
    simple_user_message_handler,
    DefaultRouter,
    SimpleBotEvent,
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
from json import loads
from os import getcwd

config_router = DefaultRouter()
config_path = getcwd().replace("\\", "/") + "/config.json"


@simple_user_message_handler(config_router, CustomCommandFilter("конфиг"))
async def config(event: SimpleBotEvent):
    with open(config_path, "r") as f:
        content = loads(f.read())
    await event.answer(
        'Токен: _______________\n'
        f'Айди: {content["user_id"]}\n'
        f'Префикс: {content["prefix"]}\n'
        f'Для всех: {"да" if content["work_for_everyone"] else "нет"}\n'
        f'Удалять после: {"не удалять" if content["delete_after"] == 0 else content["delete_after"]}\n'
        f'Время бомбы: {content["bomb_time"]}\n'
        f'Информация о человеке в лс: {"да" if content["send_info_in_dm"] else "нет"}\n'
        f'Удалять, или редактировать: {"редактировать" if content["edit_or_delete"] == "edit" else "удалять"}'
    )
