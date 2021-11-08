from vkwave.bots import (
    simple_user_message_handler, DefaultRouter,
    SimpleBotEvent
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
from json import loads
from os import getcwd
import asyncio

bomb_router = DefaultRouter()
config_path = getcwd()+'/config.json'

@simple_user_message_handler(bomb_router, CustomCommandFilter("бомба "))
async def bomb(event: SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:])
    with open(config_path, "r") as f:
        content = loads(f.read())
        bomb_time = content["bomb_time"]
    if content["work_for_everyone"] is not True:
        bomb_id = event.object.object.message_id
    else:
        await event.answer("абоба")
        bomb_id = event.object.object.message_id+1

    for n in range(bomb_time, 0, -1):
        await edit_msg(api_session, bomb_id, event.peer_id,
                       text=f'{message}\n\nДанное сообщение взорвется через {n} секунд! &#128163;',
                       m="bomb")
        await asyncio.sleep(1.0)
    await edit_msg(api_session, bomb_id, event.peer_id,
                   text='БУМ! Взрывная беседа!! &#128165;&#128165;')