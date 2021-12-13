from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from utils.emojis import enabled, disabled, error
from filters import ForEveryoneRule
import json


bp = Blueprint("Settings command")


# Настройки
@bp.on.message(ForEveryoneRule("settings"), text="<prefix>для всех <command>")
async def for_everyone_handler(message: Message, command):
    with open("commands_for_everyone.json", "r") as f:
        content = json.load(f)

    if command == "default":
        with open("commands_for_everyone.json", "w") as f:
            content = {
                "advancements": True,
                "blank": True,
                "bomb": True,
                "code": False,
                "demotivator": True,
                "info": True,
                "interactive_commands": True,
                "ping": True,
                "random_case": True,
                "settings": False,
                "show_config": False,
            }
            f.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            f"{enabled} | Настройки для всех вернуты к значению по умолчанию",
        )
        return

    elif command == "none":
        with open("commands_for_everyone.json", "w") as f:
            for command in content:
                content[command] = False
            f.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api, message, f"{disabled} | Все команды для всех выключены"
        )
        return

    if command not in content:
        await edit_msg(bp.api, message, f"{error} | Такой команды нет ")
        return

    if content[command]:
        content[command] = False
        with open("commands_for_everyone.json", "w") as f:
            content[command] = False
            f.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api, message, f"{disabled} | Команда {command} отключена "
        )
    else:
        content[command] = True
        with open("commands_for_everyone.json", "w") as f:
            content[command] = True
            f.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            f"Команда {command} включена " + enabled,
        )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>для всех")
async def show_for_everyone_handler(message: Message):
    with open("commands_for_everyone.json", "r") as f:
        content = json.load(f)
    text = "Команды для всех:\n"
    for command in content:
        if content[command]:
            text += f"{command} | {enabled}\n"
        else:
            text += f"{command} | {disabled}\n"
    await edit_msg(bp.api, message, text)


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>время бомбы <time>")
async def set_bomb_time_handler(message: Message, time):
    try:
        time = int(time)
    except ValueError:
        await edit_msg(
            bp.api,
            message,
            "Время бомбы - не число! " + error,
        )
        return

    if time < 1:
        await edit_msg(
            bp.api,
            message,
            "Время бомбы не может быть меньше 1! " + error,
        )
    else:
        with open("config.json", "r") as f:
            content = json.load(f)
        with open("config.json", "w") as f:
            content["bomb_time"] = int(message.text.split()[2])
            f.write(json.dumps(content, indent=4))

        await edit_msg(
            bp.api,
            message,
            f"{enabled} | Время бомбы изменено на "
            f"{content['bomb_time']} секунд ",
        )


@bp.on.message(
    ForEveryoneRule("settings"), text="<prefix>время удаления <time>"
)
async def set_delete_time_handler(message: Message, time):
    try:
        time = int(time)
    except ValueError:
        await edit_msg(
            bp.api,
            message,
            "Время удаления - не число! " + error,
        )
        return

    if time < 0:
        await edit_msg(
            bp.api,
            message,
            "Время удаления не может быть меньше 0! " + error,
        )
    else:
        with open("config.json", "r") as f:
            content = json.load(f)
        with open("config.json", "w") as f:
            content["delete_after"] = int(message.text.split()[2])
            f.write(json.dumps(content, indent=4))

        await edit_msg(
            bp.api,
            message,
            f"{enabled} | Время удаления изменено на "
            f"{content['delete_after']} секунд",
        )


@bp.on.message(
    ForEveryoneRule("settings"), text="<prefix>префикс <prefix_new>"
)
async def set_prefix_handler(message: Message, prefix_new):
    with open("config.json", "r") as f:
        content = json.load(f)
    with open("config.json", "w") as f:
        content["prefix"] = prefix_new
        f.write(json.dumps(content, indent=4))
    await edit_msg(
        bp.api,
        message,
        f'{enabled} | Ваш префикс изменился на "{content["prefix"]}"!',
    )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>инфо лс")
async def info_in_dm_handler(message: Message):
    with open("config.json", "r") as f:
        content = json.load(f)

    f = open("config.json", "w")
    if content["send_info_in_dm"]:
        content["send_info_in_dm"] = False
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message,
            "&#128101; | Теперь информация будет присылаться в чат",
        )

    else:
        content["send_info_in_dm"] = True
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message,
            "&#128100; | Теперь информация будет присылаться в лс",
        )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>ред")
async def edit_or_del_handler(message: Message):
    with open("config.json", "r") as f:
        content = json.load(f)

    f = open("config.json", "w")
    if content["edit_or_send"] == "edit":
        content["edit_or_send"] = "send"
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message,
            f"{disabled} | Теперь сообщения будут отправляться, а не "
            "редактироваться",
        )

    else:
        content["edit_or_send"] = "edit"
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message,
            f"{enabled} | Теперь сообщения будут редактироваться, а не "
            "отправляться",
        )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>debug")
async def debug_mode_handler(message: Message):
    with open("config.json", "r") as f:
        content = json.load(f)

    f = open("config.json", "w")
    if content["debug"]:
        content["debug"] = False
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(bp.api, message, f"{disabled} | Debug-режим выключен")

    else:
        content["debug"] = True
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(bp.api, message, f"{enabled} | Debug-режим включен")
