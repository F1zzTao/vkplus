"""
Эта команда позволяет интерпретировать Python-код
"""
from vkbottle.bot import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule


bp = Blueprint("Code executer command")


# pylint: disable=exec-used, broad-except
@bp.on.message(ForEveryoneRule("code"), text="<prefix>код<!>\n<!>")
async def code_handler(message: Message):
    """
    > !код
    > a = 5
    > b = 10
    > if b > a:
    >     c = b + a

    > a: int = 5
    > b: int = 10
    > c: int = 15
    """
    code = '\n'.join(message.text.split("\n")[1:])
    locals_ = {"message": message, "bp": bp}
    text = ""
    try:
        exec(code.replace("~", " "), None, locals_)
    except Exception as exc:
        await edit_msg(bp.api, message, exc)
        return

    for key, var in locals_.items():
        if key not in ("message", "bp"):
            text += f"{key}: {type(var).__name__} = {var}\n"
    await edit_msg(bp.api, message, text)
