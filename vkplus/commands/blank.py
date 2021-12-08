from vkbottle.bot import Blueprint, Message

from utils.edit_msg import edit_msg
import re


bp = Blueprint("Blank message")


@bp.on.message(text="<prefix>пустое <text>")
async def empty_message(message: Message, text):
    text = re.sub(r"\w", "&#10240;", text).replace(
        "<&#10240;&#10240;>", "\n"
    )
    await edit_msg(
        bp.api, message.id, message.peer_id, text=text
    )
