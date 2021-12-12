from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from utils.emojis import enabled, disabled, error
import json


bp = Blueprint("Settings command")


# Настройки
@bp.on.message(text="<prefix>для всех")
async def for_everyone(message: Message):
    with open("config.json", "r") as f:
        content = json.loads(f.read())
    if content["work_for_everyone"] is False:
        with open("config.json", "w") as f:
            content["work_for_everyone"] = True
            f.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            "Команды для всех включены " + enabled,
        )

    else:
        with open("config.json", "w") as f:
            content["work_for_everyone"] = False
            f.write(json.dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            "Команды для всех выключены " + disabled,
        )


@bp.on.message(text="<prefix>время бомбы <time>")
async def set_bomb_time(message: Message, time):
    try:
        time = int(time)
        if time < 1:
            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text="Время бомбы не может быть меньше 1! " + error,
            )
        else:
            with open("config.json", "r") as f:
                content = json.loads(f.read())
            with open("config.json", "w") as f:
                content["bomb_time"] = int(message.text.split()[2])
                f.write(json.dumps(content, indent=4))

            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text=(
                    "Время бомбы изменено на "
                    f"{content['bomb_time']} секунд " + enabled
                )
            )

    except ValueError:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Время бомбы - не число! " + error,
        )


@bp.on.message(text="<prefix>время удаления <time>")
async def set_delete_time(message: Message, time):
    try:
        time = int(time)
    except ValueError:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Время удаления - не число! " + error
        )
        return

    if time < 0:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Время удаления не может быть меньше 0! " + error,
        )
    else:
        with open("config.json", "r") as f:
            content = json.loads(f.read())
        with open("config.json", "w") as f:
            content["delete_after"] = int(message.text.split()[2])
            f.write(json.dumps(content, indent=4))

        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text=(
                "Время удаления изменено на "
                f"{content['delete_after']} секунд " + enabled
            )
        )


@bp.on.message(text="<prefix>префикс <prefix_new>")
async def set_prefix(message: Message, prefix_new):
    with open("config.json", "r") as f:
        content = json.loads(f.read())
    with open("config.json", "w") as f:
        content["prefix"] = prefix_new
        f.write(json.dumps(content, indent=4))
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        text=f'Ваш префикс изменился на "{content["prefix"]}"! ' + enabled
    )


@bp.on.message(text="<prefix>инфо лс")
async def info_in_dm(message: Message):
    with open("config.json", "r") as f:
        content = json.loads(f.read())

    f = open("config.json", "w")
    if content["send_info_in_dm"]:
        content["send_info_in_dm"] = False
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь информация будет присылаться в чат &#128101;",
        )

    else:
        content["send_info_in_dm"] = True
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь информация будет присылаться в лс &#128100;",
        )


@bp.on.message(text="<prefix>ред")
async def edit_or_del(message: Message):
    with open("config.json", "r") as f:
        content = json.loads(f.read())

    f = open("config.json", "w")
    if content["edit_or_send"] == "edit":
        content["edit_or_send"] = "send"
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь сообщения будут отправляться, а не редактироваться "
            + disabled,
        )

    else:
        content["edit_or_send"] = "edit"
        f.write(json.dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь сообщения будут "
            "редактироваться, а не отправляться " + enabled
        )
