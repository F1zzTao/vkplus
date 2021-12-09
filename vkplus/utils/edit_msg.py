from json import loads
import asyncio


# Метод для красивого редактированяи сообщения
async def edit_msg(
    api_session, msg_id, peer_id, text="", attachment=None, m=None
):
    with open("config.json", "r") as f:
        content = loads(f.read())

    if content["edit_or_send"] == "edit" or m is not None:
        await api_session.messages.edit(
            message=text,
            peer_id=peer_id,
            attachment=attachment,
            message_id=msg_id,
            keep_forward_messages=1,
        )

    else:
        msg_id = await api_session.messages.send(
            peer_id=peer_id, message=text, attachment=attachment, random_id=0
        )

    if content["delete_after"] != 0 and m is None:
        await asyncio.sleep(content["delete_after"])
        await api_session.messages.delete(
            peer_id=peer_id, message_ids=msg_id, delete_for_all=1
        )
