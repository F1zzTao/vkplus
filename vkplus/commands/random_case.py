from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule
from random import randint


bp = Blueprint("Random case command")


# > !рандом какой-то текст
# > кАкОЙ-ТО тЕкСт
@bp.on.message(ForEveryoneRule("random_case"), text="<prefix>рандом <!>")
async def random_case(message: Message):
    text = message.text.split(" ")[1]
    new_message = ""
    for letter in text:
        if randint(0, 1) == 1:
            new_message += letter.upper()
        else:
            new_message += letter
    await edit_msg(bp.api, message, text=new_message)
