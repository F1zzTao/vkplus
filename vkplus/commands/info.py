from vkwave.bots import (
    simple_user_message_handler, DefaultRouter, SimpleBotEvent
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.emojis import error
from utils.apisession import api_session
from json import loads
from inspect import cleandoc
from os import getcwd

info_router = DefaultRouter()
config_path = getcwd()+'/config.json'

@simple_user_message_handler(info_router, CustomCommandFilter("инфо"))
async def show_info(event: SimpleBotEvent) -> str:
    if len(event.object.object.text.split()) > 1:
        if event.object.object.text.split()[1].startswith("["):
            mention = event.object.object.text.split()[1]
            show_about = mention.split("|")[0][1:].replace("id","")
    elif 'reply' in event.object.object.extra_message_data:
        conv_msg_id = loads(event.object.object.extra_message_data['reply'])['conversation_message_id']
        show_about = await api_session.messages.get_by_conversation_message_id(peer_id=event.peer_id,
                                                                               conversation_message_ids=conv_msg_id)
        show_about = show_about.response.items[0].from_id
    else:
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text='Вы не ответили никому! '+error)
        return

    show_info = await api_session.users.get(user_ids=show_about, name_case="abl",
                                            fields=cleandoc("""sex,bdate,city,
                                            country,online,domain,status,
                                            followers_count,can_post,
                                            can_write_private_message,
                                            can_send_friend_request,is_friend,
                                            blacklisted,blacklisted_by_me,
                                            can_be_invited_group,counters""").replace("\n",""))
    show_info = show_info.response[0]

    text = cleandoc(f"""Информация о [id{show_info.id}|{show_info.first_name} {show_info.last_name}] &#128101;:
                    Айди: {show_info.id}
                    Отображаемый никнейм: {show_info.domain}
                    Пол: {"мужской &#9794;" if show_info.sex.name == "MALE" else "женский &#9792;" if show_info.sex.name == "FEMALE" else show_info.sex}
                    День рождения: {"скрыто" if show_info.bdate is None else show_info.bdate} &#127874;
                    Город: {"скрыто" if show_info.city is None else show_info.city.title} &#127961;
                    Страна: {show_info.country.title if show_info.country is not None else "скрыто"} &#127970;
                    Онлайн: {"да &#127934;" if show_info.online.value == 1 else "нет &#127936;"}
                    Статус: {show_info.status}
                    Закрытая страница: {"да &#9940;" if show_info.is_closed else "нет &#9989;"}
                    Друг: {"друг" if show_info.is_friend.value == 1 else "недруг("}
                    Стена открыта: {"да &#10004;" if show_info.can_post.value == 1 else "нет &#128683;"}
                    Подписчиков: {"не известно" if show_info.followers_count is None else show_info.followers_count}
                    Друзей: {"не известно" if show_info.counters is None else show_info.counters.friends}""")

    with open(config_path, "r") as f:
        content = loads(f.read())

    if content["send_info_in_dm"] is True:
        await api_session.messages.send(peer_id=content["user_id"], message=text, random_id=0)
    else:
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text=text)