from vkwave.bots import (
    simple_user_message_handler,
    DefaultRouter,
    SimpleBotEvent,
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
from json import loads
from utils.emojis import error

interactive_router = DefaultRouter()


@simple_user_message_handler(interactive_router, CustomCommandFilter("me "))
async def me(event: SimpleBotEvent) -> str:
    action = " ".join(event.object.object.text.split()[1:])
    who = await api_session.users.get(
        user_ids=event.object.object.message_data.from_id
    )
    name = who.response[0].first_name
    last_name = who.response[0].last_name
    await edit_msg(
        api_session,
        event.object.object.message_id,
        event.peer_id,
        text=f"{name} {last_name} {action} &#128172;",
    )


@simple_user_message_handler(
    interactive_router, CustomCommandFilter("бонкнуть")
)
async def bonk(event: SimpleBotEvent) -> str:
    if len(event.object.object.text.split()) > 1:
        if event.object.object.text.split()[1].startswith("["):
            mention = event.object.object.text.split()[1]
            bonk_who = mention.split("|")[0][1:].replace("id", "")
    elif "reply" in event.object.object.extra_message_data:
        conv_msg_id = loads(event.object.object.extra_message_data["reply"])[
            "conversation_message_id"
        ]
        bonk_who = await api_session.messages.get_by_conversation_message_id(
            peer_id=event.peer_id, conversation_message_ids=conv_msg_id
        )
        bonk_who = bonk_who.response.items[0].from_id
    else:
        await edit_msg(
            api_session,
            event.object.object.message_id,
            event.peer_id,
            text="Вы не ответили никому! " + error,
        )
        return

    bonk_who_info = await api_session.users.get(
        user_ids=bonk_who, name_case="acc"
    )
    bonk_who_name = bonk_who_info.response[0].first_name
    bonk_who_last_name = bonk_who_info.response[0].last_name

    who_bonks = await api_session.users.get(
        user_ids=event.object.object.message_data.from_id
    )
    name = who_bonks.response[0].first_name
    last_name = who_bonks.response[0].last_name
    await edit_msg(
        api_session,
        event.object.object.message_id,
        event.peer_id,
        text=(
            f"{name} {last_name} бонкнул"
            f" [id{bonk_who}|{bonk_who_name} {bonk_who_last_name}] &#129529;"
        ),
    )


@simple_user_message_handler(
    interactive_router, CustomCommandFilter("бросить кактус")
)
async def cactus(event: SimpleBotEvent) -> str:
    if len(event.object.object.text.split()) > 2:
        if event.object.object.text.split()[2].startswith("["):
            mention = event.object.object.text.split()[2]
            throw_to = mention.split("|")[0][1:].replace("id", "")
    elif "reply" in event.object.object.extra_message_data:
        conv_msg_id = loads(event.object.object.extra_message_data["reply"])[
            "conversation_message_id"
        ]
        throw_to = await api_session.messages.get_by_conversation_message_id(
            peer_id=event.peer_id, conversation_message_ids=conv_msg_id
        )
        throw_to = throw_to.response.items[0].from_id
    else:
        await edit_msg(
            api_session,
            event.object.object.message_id,
            event.peer_id,
            text="Вы не ответили никому! " + error,
        )
        return

    throw_to_info = await api_session.users.get(
        user_ids=throw_to, name_case="acc"
    )
    throw_to_name = throw_to_info.response[0].first_name
    throw_to_last_name = throw_to_info.response[0].last_name

    who_throws = await api_session.users.get(
        user_ids=event.object.object.message_data.from_id
    )
    name = who_throws.response[0].first_name
    last_name = who_throws.response[0].last_name
    await edit_msg(
        api_session,
        event.object.object.message_id,
        event.peer_id,
        text=(
            f"{name} {last_name} бросил кактус в"
            f" [id{throw_to}|{throw_to_name} {throw_to_last_name}] &#127797;"
        ),
    )
