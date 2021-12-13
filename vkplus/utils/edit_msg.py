from vkbottle.user import Message
import json
import asyncio


# Метод для красивого редактированяи сообщения
async def edit_msg(
    api_session,
    message: Message,
    text=None,
    attachment=None,
    m=None,
    bomb_id=None
):
    with open("config.json", "r") as f:
        content = json.load(f)
    if (
        message.from_id == int(content["user_id"])
        and content["edit_or_send"] == "edit"
        or m is not None
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

    if content["delete_after"] != 0 and m is None:
        await asyncio.sleep(content["delete_after"])
        await api_session.messages.delete(
            peer_id=message.peer_id,
            message_ids=(message.id if bomb_id is None else bomb_id),
            delete_for_all=1,
        )
