from vkbottle.user import Blueprint, Message

from typing import Optional
from utils.edit_msg import edit_msg
from utils.emojis import error
from json import loads
from inspect import cleandoc

bp = Blueprint("Info command")


@bp.on.message(text=["<prefix>инфо", "<prefix>инфо <mention>"])
async def show_info(message: Message, mention: Optional[str] = None):
    if mention is not None:
        show_about = mention.split("|")[0][1:].replace("id", "")
    elif message.reply_message is not None:
        show_about = message.reply_message.from_id
    else:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Вы не ответили никому! " + error,
        )
        return

    show_info = await bp.api.users.get(
        user_ids=show_about,
        name_case="abl",
        fields=cleandoc(
            """sex,bdate,city,
            country,online,domain,status,
            followers_count,can_post,
            can_write_private_message,
            can_send_friend_request,is_friend,
            blacklisted,blacklisted_by_me,
            can_be_invited_group,counters"""
        ).replace("\n", ""),
    )
    show_info = show_info[0]

    text = cleandoc(
        f"""Информация о [id{show_info.id}|{show_info.first_name} {show_info.last_name}] &#128101;:
                    Айди: {show_info.id}
                    Отображаемый никнейм: {show_info.domain}
                    Пол: {"мужской &#9794;" if show_info.sex == 2 else "женский &#9792;" if show_info.sex == 1 else show_info.sex}
                    День рождения: {"скрыто" if show_info.bdate is None else show_info.bdate} &#127874;
                    Город: {"скрыто" if show_info.city is None else show_info.city.title} &#127961;
                    Страна: {show_info.country.title if show_info.country is not None else "скрыто"} &#127970;
                    Онлайн: {"да &#127934;" if show_info.online.value == 1 else "нет &#127936;"}
                    Статус: {show_info.status}
                    Закрытая страница: {"да &#9940;" if show_info.is_closed else "нет &#9989;"}
                    Друг: {"друг" if show_info.is_friend.value == 1 else "недруг("}
                    Стена открыта: {"да &#10004;" if show_info.can_post.value == 1 else "нет &#128683;"}
                    Подписчиков: {"не известно" if show_info.followers_count is None else show_info.followers_count}
                    Друзей: {"не известно" if show_info.counters is None else show_info.counters.friends}"""  # noqa: E501
    )

    with open("config.json", "r") as f:
        content = loads(f.read())

    if content["send_info_in_dm"] is True:
        await bp.api.messages.send(
            peer_id=content["user_id"], message=text, random_id=0
        )
    else:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text=text,
        )
