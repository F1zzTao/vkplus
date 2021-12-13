from vkbottle.bot import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule


bp = Blueprint("Code executer command")


# > !код
# > a = 5
# > b = 10
# > if b > a:
# >     c = b + a

# > a: 5
# > b: 10
# > c: 15
@bp.on.message(ForEveryoneRule("code"), text="<prefix>код<!>\n<!>")
async def code_handler(message: Message):
    code = '\n'.join(message.text.split("\n")[1:])
    print(code)
    locals_ = {}
    text = ""
    try:
        exec(code.replace("~", " "), None, locals_)
        for key, var in locals_.items():
            text += f"{key}: {var}\n"
        await edit_msg(bp.api, message, text)
    except Exception as exc:
        await edit_msg(bp.api, message, exc)
