"""
Здесь собраны все команды настроек
"""
import json
from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from utils.emojis import ENABLED, DISABLED, ERROR
from filters import ForEveryoneRule


bp = Blueprint("Settings command")


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>для всех <command>")
async def for_everyone_handler(message: Message, command):
    """
    Команда для изменения доступности других команд для других людей
    """
    with open("commands_for_everyone.json", "r", encoding="utf-8") as file:
        content = json.load(file)

    if command == "default":
        with open("commands_for_everyone.json", "w", encoding="utf-8") as file:
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
            file.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            f"{ENABLED} | Настройки для всех вернуты к значению по умолчанию",
        )

    elif command == "none":
        with open("commands_for_everyone.json", "w", encoding="utf-8") as file:
            for allowed_command in content:
                content[allowed_command] = False
            file.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api, message, f"{DISABLED} | Все команды для всех выключены"
        )

    elif command not in content:
        await edit_msg(bp.api, message, f"{ERROR} | Такой команды нет ")

    else:
        if content[command]:
            content[command] = False
            with open(
                "commands_for_everyone.json", "w", encoding="utf-8"
            ) as file:
                content[command] = False
                file.write(json.dumps(content, indent=4))
            await edit_msg(
                bp.api, message, f"{DISABLED} | Команда {command} отключена "
            )
        else:
            content[command] = True
            with open(
                "commands_for_everyone.json", "w", encoding="utf-8"
            ) as file:
                content[command] = True
                file.write(json.dumps(content, indent=4))
            await edit_msg(
                bp.api,
                message,
                f"Команда {command} включена " + ENABLED,
            )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>для всех")
async def show_for_everyone_handler(message: Message):
    """
    Команда для проверки доступности команд для других людей
    """
    with open("commands_for_everyone.json", "r", encoding="utf-8") as file:
        content = json.load(file)
    text = "Команды для всех:\n"
    for command in content:
        if content[command]:
            text += f"{command} | {ENABLED}\n"
        else:
            text += f"{command} | {DISABLED}\n"
    await edit_msg(bp.api, message, text)


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>время бомбы <time>")
async def set_bomb_time_handler(message: Message, time):
    """
    Команда для настройки времени бомбы (!бомба)
    """
    try:
        time = int(time)
    except ValueError:
        await edit_msg(
            bp.api,
            message,
            "Время бомбы - не число! " + ERROR,
        )
        return

    if time < 1:
        await edit_msg(
            bp.api,
            message,
            "Время бомбы не может быть меньше 1! " + ERROR,
        )
    else:
        with open("config.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        with open("config.json", "w", encoding="utf-8") as file:
            content["bomb_time"] = int(message.text.split()[2])
            file.write(json.dumps(content, indent=4))

        await edit_msg(
            bp.api,
            message,
            f"{ENABLED} | Время бомбы изменено на "
            f"{content['bomb_time']} секунд ",
        )


@bp.on.message(
    ForEveryoneRule("settings"), text="<prefix>время удаления <time>"
)
async def set_delete_time_handler(message: Message, time):
    """
    Команда для настройки времени удаления всех выполненных команд
    """
    try:
        time = int(time)
    except ValueError:
        await edit_msg(
            bp.api,
            message,
            "Время удаления - не число! " + ERROR,
        )
        return

    if time < 0:
        await edit_msg(
            bp.api,
            message,
            "Время удаления не может быть меньше 0! " + ERROR,
        )
    else:
        with open("config.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        with open("config.json", "w", encoding="utf-8") as file:
            content["delete_after"] = int(message.text.split()[2])
            file.write(json.dumps(content, indent=4))

        await edit_msg(
            bp.api,
            message,
            f"{ENABLED} | Время удаления изменено на "
            f"{content['delete_after']} секунд",
        )


@bp.on.message(
    ForEveryoneRule("settings"), text="<prefix>префикс <prefix_new>"
)
async def set_prefix_handler(message: Message, prefix_new):
    """
    Команда для изменения префикса бота
    """
    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)
    with open("config.json", "w", encoding="utf-8") as file:
        content["prefix"] = prefix_new
        file.write(json.dumps(content, indent=4))
    await edit_msg(
        bp.api,
        message,
        f'{ENABLED} | Ваш префикс изменился на "{content["prefix"]}"!',
    )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>инфо лс")
async def info_in_dm_handler(message: Message):
    """
    Команда для изменения отправки информации о людях (!инфо)
    """
    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)

    if content["send_info_in_dm"]:
        content["send_info_in_dm"] = False
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            "&#128101; | Теперь информация будет присылаться в чат",
        )

    else:
        content["send_info_in_dm"] = True
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            "&#128100; | Теперь информация будет присылаться в лс",
        )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>ред")
async def edit_or_del_handler(message: Message):
    """
    Команда для выбора - редактировать, или удалять команды
    """
    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)

    if content["edit_or_send"] == "edit":
        content["edit_or_send"] = "send"
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            f"{DISABLED} | Теперь сообщения будут отправляться, а не "
            "редактироваться",
        )

    else:
        content["edit_or_send"] = "edit"
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message,
            f"{ENABLED} | Теперь сообщения будут редактироваться, а не "
            "отправляться",
        )


@bp.on.message(ForEveryoneRule("settings"), text="<prefix>debug")
async def debug_mode_handler(message: Message):
    """
    Команда для включения и выключения режима debug
    """
    with open("config.json", "r", encoding="utf-8") as file:
        content = json.load(file)

    if content["debug"]:
        content["debug"] = False
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
        await edit_msg(bp.api, message, f"{DISABLED} | Debug-режим выключен")

    else:
        content["debug"] = True
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
        await edit_msg(bp.api, message, f"{ENABLED} | Debug-режим включен")
