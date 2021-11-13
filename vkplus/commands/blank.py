from vkwave.bots import (
    simple_user_message_handler,
    DefaultRouter,
    SimpleBotEvent,
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
import re

blank_router = DefaultRouter()


@simple_user_message_handler(blank_router, CustomCommandFilter("пустое "))
async def empty_message(event: SimpleBotEvent) -> str:
    message = " ".join(event.object.object.text.split()[1:])
    text = re.sub(r"\w", "&#10240;", message).replace(
        "<&#10240;&#10240;>", "\n"
    )
    await edit_msg(
        api_session, event.object.object.message_id, event.peer_id, text=text
    )
