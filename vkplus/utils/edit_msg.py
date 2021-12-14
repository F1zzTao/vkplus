"""
Method for editing message
"""
import json
import asyncio
from vkbottle.user import Message


# pylint: disable=too-many-arguments
async def edit_msg(
    api_session,
    message: Message,
    text=None,
    attachment=None,
    mode=None,
    bomb_id=None,
):
    """
    Метод для красивого редактирования сообщения
    """
    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)
    if (
        message.from_id == int(content["user_id"])
        and content["edit_or_send"] == "edit"
        or mode is not None
    ):
        await api_session.messages.edit(
            message=text,
            peer_id=message.peer_id,
            attachment=attachment,
            message_id=(message.id if bomb_id is None else bomb_id),
            keep_forward_messages=1,
        )

    else:
        message.id = await api_session.messages.send(
            peer_id=message.peer_id,
            message=text,
            attachment=attachment,
            random_id=0,
        )

    if content["delete_after"] != 0 and mode is None:
        await asyncio.sleep(content["delete_after"])
        await api_session.messages.delete(
            peer_id=message.peer_id,
            message_ids=(message.id if bomb_id is None else bomb_id),
            delete_for_all=1,
        )
