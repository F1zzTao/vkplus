from vkbottle.user import Blueprint, Message

from typing import Optional
from utils.edit_msg import edit_msg
from utils.emojis import error
from filters import NotSettingRule
from filters import ForEveryoneRule
import json

bp = Blueprint("Info command")


@bp.on.message(
    NotSettingRule(),
    ForEveryoneRule("info"),
    text=["<prefix>инфо", "<prefix>инфо <mention>"],
)
async def show_info(message: Message, mention: Optional[str] = None):
    if mention is not None:
        show_about = mention.split("|")[0][1:].replace("id", "")
    elif message.reply_message is not None:
        show_about = message.reply_message.from_id
    else:
        await edit_msg(
            bp.api, message, text=f"{error} | Вы не ответили никому!"
        )
        return
    show_info = await bp.api.users.get(
        user_ids=show_about,
        name_case="abl",
        fields=(
            "sex,bdate,city,country,online,domain,status,"
            "followers_count,can_post,can_write_private_message,"
            "can_send_friend_request,is_friend,blacklisted,"
            "blacklisted_by_me,can_be_invited_group,counters".replace("\n", "")
        ),
    )
    show_info = show_info[0]

    text = (
        f"&#128101; | Информация о [id{show_info.id}|{show_info.first_name} {show_info.last_name}]:\n"  # noqa E501
        f"Айди: {show_info.id}\n"
        f"Отображаемый никнейм: {show_info.domain}\n"
        f'Пол: {"мужской &#128104;" if show_info.sex == 2 else "женский &#128105;" if show_info.sex == 1 else show_info.sex}\n'  # noqa E501
        f'&#127874; | День рождения: {"скрыто" if show_info.bdate is None else show_info.bdate}\n'  # noqa E501
        f'&#127961; | Город: {"скрыто" if show_info.city is None else show_info.city.title}\n'  # noqa E501
        f'&#127970; | Страна: {show_info.country.title if show_info.country is not None else "скрыто"}\n'  # noqa E501
        f'Онлайн: {"да &#127934;" if show_info.online.value == 1 else "нет &#127936;"}\n'  # noqa E501
        f"Статус: {show_info.status}\n"
        f'Закрытая страница: {"да &#9940;" if show_info.is_closed else "нет &#9989;"}\n'  # noqa E501
        f'Друг: {"друг" if show_info.is_friend.value == 1 else "недруг("}\n'
        f'Стена открыта: {"да &#10004;" if show_info.can_post.value == 1 else "нет &#128683;"}\n'  # noqa E501
        f'Подписчиков: {"не известно" if show_info.followers_count is None else show_info.followers_count}\n'  # noqa E501
        f'Друзей: {"не известно" if show_info.counters is None else show_info.counters.friends}'  # noqa E501
    )

    with open("config.json", "r") as f:
        content = json.load(f)

    if content["send_info_in_dm"] is True:
        await bp.api.messages.send(
            peer_id=content["user_id"], message=text, random_id=0
        )
    else:
        await edit_msg(bp.api, message, text=text)
