from json import loads
import asyncio
from vkwave.api.methods._error import APIError
from os import getcwd

config_path = getcwd().replace("\\", "/") + "/config.json"


# Метод для красивого редактированяи сообщения
async def edit_msg(
    api_session, msg_id, peerid, text="", attachment=None, m=None
):
    try:
        with open(config_path, "r") as f:
            edit_or_del = loads(f.read())["edit_or_delete"]

        if edit_or_del == "edit" or m is not None:
            await api_session.messages.edit(
                message=text,
                peer_id=peerid,
                attachment=attachment,
                message_id=msg_id,
                keep_forward_messages=1,
            )
            with open(config_path, "r") as f:
                time = loads(f.read())["delete_after"]
            if time != 0 and m is None:
                await asyncio.sleep(time)
                await api_session.messages.delete(
                    peer_id=peerid, message_ids=msg_id, delete_for_all=1
                )
        else:
            raise APIError(0, "", {})

    except APIError:
        await api_session.messages.send(
            message=text, peer_id=peerid, attachment=attachment, random_id=0
        )
