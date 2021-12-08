from vkbottle.user import Blueprint, Message

from typing import Optional
from utils.edit_msg import edit_msg
from utils.emojis import error

bp = Blueprint("Interactive commands")


@bp.on.message(text="<prefix>me <action>")
async def me(message: Message, action):
    who = await bp.api.users.get(user_ids=message.from_id)
    name = who[0].first_name
    last_name = who[0].last_name
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        text=f"{name} {last_name} {action} &#128172;",
    )


@bp.on.message(text=["<prefix>бонкнуть", "<prefix>бонкнуть <mention>"])
async def bonk(message: Message, mention: Optional[str] = None):
    if mention is not None:
        if mention.startswith("["):
            mention = message.text.split()[1]
            bonk_who = mention.split("|")[0][1:].replace("id", "")

        else:
            await edit_msg(
                bp.api,
                message.message_id,
                message.peer_id,
                text="Вы написали не упоминание, а какую ту чушь! " + error,
            )
            return

    elif message.reply_message is not None:
        conv_msg_id = message.reply_message.conversation_message_id
        bonk_who = await bp.api.messages.get_by_conversation_message_id(
            peer_id=message.peer_id, conversation_message_ids=conv_msg_id
        )
        bonk_who = bonk_who.items[0].from_id

    else:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Вы не ответили никому! " + error,
        )
        return

    bonk_who_info = await bp.api.users.get(user_ids=bonk_who, name_case="acc")

    bonk_who_name = bonk_who_info[0].first_name
    bonk_who_last_name = bonk_who_info[0].last_name

    who_bonks = await bp.api.users.get(user_ids=message.from_id)
    name = who_bonks[0].first_name
    last_name = who_bonks[0].last_name
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        text=(
            f"{name} {last_name} бонкнул "
            f"[id{bonk_who}|{bonk_who_name} {bonk_who_last_name}] &#129529;"
        ),
    )


@bp.on.message(
    text=["<prefix>бросить кактус", "<prefix>бросить кактус <mention>"]
)
async def cactus(message: Message, mention: Optional[str] = None):
    if mention is not None:
        if mention.startswith("["):
            mention = message.text.split()[2]
            throw_to = mention.split("|")[0][1:].replace("id", "")

        else:
            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text="Вы написали не упоминание, а какую ту чушь! " + error,
            )
            return

    elif message.reply_message is not None:
        conv_msg_id = message.reply_message.conversation_message_id
        throw_to = await bp.api.messages.get_by_conversation_message_id(
            peer_id=message.peer_id, conversation_message_ids=conv_msg_id
        )
        throw_to = throw_to.items[0].from_id

    else:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Вы не ответили никому! " + error,
        )
        return

    throw_to_info = await bp.api.users.get(user_ids=throw_to, name_case="acc")
    throw_to_name = throw_to_info[0].first_name
    throw_to_last_name = throw_to_info[0].last_name

    who_throws = await bp.api.users.get(user_ids=message.from_id)
    name = who_throws[0].first_name
    last_name = who_throws[0].last_name
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        text=(
            f"{name} {last_name} бросил кактус в "
            f"[id{throw_to}|{throw_to_name} {throw_to_last_name}] &#127797;"
        ),
    )
