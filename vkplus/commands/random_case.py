from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from random import randint


bp = Blueprint("Random case command")


@bp.on.message(text="<prefix>рандом <text>")
async def random_case(message: Message, text):
    text = text.replace("<br>", "\n")
    new_message = ""
    for letter in text:
        if randint(0, 1) == 1:
            new_message += letter.upper()
        else:
            new_message += letter
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        text=new_message,
    )
