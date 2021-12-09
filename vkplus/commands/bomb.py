from vkbottle.user import Blueprint, Message
from utils.edit_msg import edit_msg
from json import loads
import asyncio

bp = Blueprint("Bomb generator")


@bp.on.message(text="<prefix>бомба <text>")
async def bomb(message: Message, text):
    with open("config.json", "r") as f:
        content = loads(f.read())
        bomb_time = content["bomb_time"]
    if content["work_for_everyone"] is not True or message.from_id == int(
        content["user_id"]
    ):
        bomb_id = message.id
    else:
        bomb_id = await message.answer("абоба")

    for n in range(bomb_time, 0, -1):
        await edit_msg(
            bp.api,
            bomb_id,
            message.peer_id,
            text=(
                f"{text}\n\nДанное сообщение взорвется через {n} секунд! "
                "&#128163;"
            ),
            m="bomb",
        )
        await asyncio.sleep(1.0)
    await edit_msg(
        bp.api,
        bomb_id,
        message.peer_id,
        text="БУМ! Взрывная беседа!! &#128165;&#128165;"
    )
