from vkwave.bots import (
    simple_user_message_handler, DefaultRouter,
    SimpleBotEvent
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
from json import loads, dumps
from utils.emojis import enabled, disabled, error
from os import getcwd

settings_router = DefaultRouter()
config_path = getcwd().replace('\\','/')+'/config.json'

# Настройки
@simple_user_message_handler(settings_router, CustomCommandFilter("для всех"))
async def for_everyone(event: SimpleBotEvent):
    with open(config_path, "r") as f:
        content = loads(f.read())
    with open(config_path, "w") as f:
        if content["work_for_everyone"] is False:
            content["work_for_everyone"] = True
            f.write(dumps(content, indent=4))
            await event.answer("Команды для всех включены "+enabled)
        else:
            content["work_for_everyone"] = False
            f.write(dumps(content, indent=4))
            await event.answer("Команды для всех выключены "+disabled)


@simple_user_message_handler(settings_router, CustomCommandFilter("время бомбы "))
async def set_bomb_time(event: SimpleBotEvent):
    try:
        time = int(event.object.object.text.split()[2])
        if time < 1:
            await edit_msg(api_session, event.object.object.message_id,
                           event.peer_id,
                           text="Время бомбы не может быть меньше 1! "+error)
        else:
            with open(config_path, "r") as f:
                content = loads(f.read())
            with open(config_path, "w") as f:
                content["bomb_time"] = int(event.object.object.text.split()[2])
                f.write(dumps(content, indent=4))
            await edit_msg(api_session, event.object.object.message_id,
                           event.peer_id,
                           text=f"Время бомбы изменено на {content['bomb_time']} секунд "+enabled)
    except ValueError:
        await edit_msg(api_session, event.object.object.message_id,
                       text="Время бомбы - не число! "+error)

@simple_user_message_handler(settings_router, CustomCommandFilter("время удаления "))
async def set_delete_time(event: SimpleBotEvent):
    try:
        time = int(event.object.object.text.split()[2])
        if time < 0:
            await edit_msg(api_session, event.object.object.message_id,
                           event.peer_id,
                           text="Время удаления не может быть меньше 0! "+error)
        else:
            with open(config_path, "r") as f:
                content = loads(f.read())
            with open(config_path, "w") as f:
                content["delete_after"] = int(event.object.object.text.split()[2])
                f.write(dumps(content, indent=4))
            await edit_msg(api_session, event.object.object.message_id,
                           event.peer_id,
                           text=f"Время удаления изменено на {content['delete_after']} секунд "+enabled)
    except ValueError:
        await edit_msg(api_session, event.object.object.message_id,
                       text="Время удаления - не число! "+error)


@simple_user_message_handler(settings_router, CustomCommandFilter("префикс "))
async def set_prefix(event: SimpleBotEvent):
    with open(config_path, "r") as f:
        content = loads(f.read())
    with open(config_path, "w") as f:
        content["prefix"] = event.object.object.text.split()[1]
        f.write(dumps(content, indent=4))
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=f'Префикс изменится на "{content["prefix"]}" после перезагрузки бота '+enabled)


@simple_user_message_handler(settings_router, CustomCommandFilter("инфо лс"))
async def info_in_dm(event: SimpleBotEvent):
    with open(config_path, "r") as f:
        content = loads(f.read())

    f = open(config_path, 'w')
    if content['send_info_in_dm'] is True:
        content['send_info_in_dm'] = False
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text='Теперь информация будет присылаться в чат &#128101;')
    else:
        content['send_info_in_dm'] = True
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text='Теперь информация будет присылаться в лс &#128100;')


@simple_user_message_handler(settings_router, CustomCommandFilter("ред"))
async def info_in_dm(event: SimpleBotEvent):
    with open(config_path, "r") as f:
        content = loads(f.read())

    f = open(config_path, 'w')
    if content['edit_or_delete'] == "edit":
        content['edit_or_delete'] = "delete"
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text='Теперь сообщения будут удаляться, а не редактироваться '+disabled)
    else:
        content['edit_or_delete'] = "edit"
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text='Теперь сообщения будут редактироваться, а не удаляться '+enabled)