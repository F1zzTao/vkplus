from vkwave.bots import (
    simple_user_message_handler, DefaultRouter,
    SimpleBotEvent
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
from random import randint

random_router = DefaultRouter()

@simple_user_message_handler(random_router, CustomCommandFilter("рандом "))
async def random_case(event: SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:]).replace("<br>", "\n")
    new_message = ""
    for letter in message:
        if randint(0, 1) == 1:
            new_message += letter.upper()
        else:
            new_message += letter
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=new_message)