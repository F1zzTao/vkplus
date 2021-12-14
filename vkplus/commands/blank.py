"""
Команда, которая генерирует пустое сообщение
"""
import re
from vkbottle.bot import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule


bp = Blueprint("Blank message")


"""
> !пустое какой-то текст
> ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


@bp.on.message(ForEveryoneRule("blank"), text="<prefix>пустое <!>")
async def empty_message(message: Message):
    text = ' '.join(message.text.split()[1:])
    text = re.sub(r"\w", "⠀", text)
    await edit_msg(
        bp.api, message, text=text
    )
