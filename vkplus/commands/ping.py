from vkbottle.bot import Blueprint, Message

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule
from time import time
import json
import psutil
import platform


bp = Blueprint("Ping-pong command")


# > !пинг

# > 🏓 | Понг!
# > ⏱ | Ответ за 0.05 секунд

# (если включен режим debug)
# > 🏓 | Понг!
# > ⏱ | Ответ за 0.05 секунд (debug)
# > 💻 | ОС: Microsoft Windows 11
# > 🔧 | Процессор: 21.2%
# > ⚙ | Работает 97 часов (4 дней)
# > ❤ | [id322615766|VK+]
@bp.on.message(ForEveryoneRule("ping"), text="<prefix>пинг")
async def ping_handler(message: Message):
    start = time()
    with open("config.json", "r") as f:
        content = json.load(f)

    if content["debug"] is not True:
        end = time()
        result = round(end - start, 4)
        await edit_msg(
            bp.api,
            message,
            f"&#127955; | Понг!\n&#9201; | Ответ за {result} секунд",
        )
    else:
        try:
            cpu = str(psutil.cpu_percent()) + "%"
        except PermissionError:
            cpu = "не известно (android?)"

        system_name = platform.system()
        # На время написания этого комментария, версия kernel32.dll
        # не изменилась, из-за этого platform.release() пишет 10
        # вместо 11 на компьютере с Windows 11, поэтому здесь
        # используется такой способ:
        if system_name == "Windows":
            if int(platform.version().split(".")[2]) > 20000:
                system_version = "11"
            else:
                system_version = platform.release()
        else:
            system_version = platform.release()

        system = system_name + " " + system_version
        with open("time_started.txt", "r") as f:
            work_hours = round((round(time()) - int(f.read())) / 3600, 4)
        work_days = work_hours // 24
        end = time()
        result = round(end - start, 4)
        await edit_msg(
            bp.api, message,
            f"&#127955; | Понг!\n&#9201; | Ответ за {result} секунд (debug)\n"
            f"&#128187; | ОС: {system}\n"
            f"&#128295; | Процессор: {cpu}\n"
            f"&#9881; | Работает {work_hours} часов ({work_days} дней)\n"
            "&#10084; | [id322615766|VK+]"
        )
