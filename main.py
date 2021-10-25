import asyncio

from vkwave.bots import (
    SimpleLongPollUserBot,
    MiddlewareResult, BotEvent,
    create_api_session_aiohttp,
    PhotoUploader
)

from vkwave.bots.core.dispatching.filters.base import (
    BaseFilter, FilterResult
)
from vkwave.api.methods._error import APIError

from PIL import Image, ImageDraw, ImageFont
from json import loads, dumps
import random
import re
import requests

defaultConfig = """{
    "token": "",
    "user_id": "",
    "work_for_everyone": false,
    "prefix": "!",
    "bomb_time": 10
}
"""


def exit_from_programm(code=0):
    input("\nНажмите Enter, что бы завершить программу... ")
    raise SystemExit(code)


try:
    with open('config.json', 'r') as f:
        content = loads(f.read())
except FileNotFoundError:
    print("Конфиг не найден, я его создам, а вы заполните его...")
    with open('config.json', 'w') as f:
        f.write(defaultConfig)
        raise FileNotFoundError("Config not found")

bot = SimpleLongPollUserBot(tokens=content["token"])
api_session = create_api_session_aiohttp(content["token"]).api.get_context()
uploader = PhotoUploader(api_session)
user_id = content["user_id"]

enabled = "&#9989;"
disabled = "&#10060;"
error = "&#9888;"


# Мидлварь на проверку, является ли пользователь
# пользователем, или же нет.
@bot.middleware()
async def fromme(event: BotEvent) -> MiddlewareResult:
    if event.object.object.event_id == 4:
        with open("config.json", "r") as f:
            content = loads(f.read())
        if event.object.object.message_data.from_id == user_id:
            return MiddlewareResult(True)
        return MiddlewareResult(content["work_for_everyone"])
    return False


# Метод для красивого редактированяи сообщения
async def edit_msg(api_session, msg_id, peerid, text="", attachment=None):
    try:
        await api_session.messages.edit(message=text,
                                        peer_id=peerid,
                                        attachment=attachment,
                                        message_id=msg_id, keep_forward_messages=1)
    except APIError:
        await api_session.messages.send(message=text,
                                        peer_id=peerid,
                                        attachment=attachment,
                                        random_id=0)


# Нормальный фильтр команд
class CustomCommandFilter(BaseFilter):
    def __init__(self, message) -> None:
        self.message = message
        with open("config.json", "r") as f:
            self.content = f.read()
            self.prefix = loads(self.content)["prefix"]

    async def check(self, event: bot.SimpleBotEvent) -> FilterResult:
        text: str = event.object.object.text
        # я ненавижу pep8
        if text.startswith(self.prefix) and \
           text[len(self.prefix):].startswith(self.message):
            return FilterResult(True)
        return FilterResult(False)


"""
TODO: сделать создание достижений из майнкрафта
"""


# Настройки
@bot.message_handler(CustomCommandFilter("для всех"))
async def for_everyone(event: bot.SimpleBotEvent) -> str:
    with open("config.json", "r") as f:
        content = loads(f.read())
    with open("config.json", "w") as f:
        if content["work_for_everyone"] is False:
            content["work_for_everyone"] = True
            f.write(dumps(content, indent=4))
            await event.answer("Команды для всех включены "+enabled)
        else:
            content["work_for_everyone"] = False
            f.write(dumps(content, indent=4))
            await event.answer("Команды для всех выключены "+disabled)


@bot.message_handler(CustomCommandFilter("время бомбы "))
async def set_bomb_time(event: bot.SimpleBotEvent) -> str:
    try:
        time = int(event.object.object.text.split()[2])
        if time < 1:
            await edit_msg(api_session, event.object.object.message_id,
                           event.peer_id,
                           text="Время бомбы не может быть меньше 1! "+error)
        else:
            with open("config.json", "r") as f:
                content = loads(f.read())
            with open("config.json", "w") as f:
                content["bomb_time"] = int(event.object.object.text.split()[2])
                f.write(dumps(content, indent=4))
            await edit_msg(api_session, event.object.object.message_id,
                           event.peer_id,
                           text=f"Время бомбы изменено на {content['bomb_time']} секунд "+enabled)
    except ValueError:
        await edit_msg(api_session, event.object.object.message_id,
                       text="Время бомбы - не число! "+error)


@bot.message_handler(CustomCommandFilter("префикс "))
async def set_prefix(event: bot.SimpleBotEvent) -> str:
    with open("config.json", "r") as f:
        content = loads(f.read())
    with open("config.json", "w") as f:
        content["prefix"] = event.object.object.text.split()[1]
        f.write(dumps(content, indent=4))
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=f'Успешно установили префикс на "{content["prefix"]}" '+enabled)


# Команды
@bot.message_handler(CustomCommandFilter("пустое "))
async def empty_message(event: bot.SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:])
    text = re.sub("\w", "&#10240;", message)
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=text)


@bot.message_handler(CustomCommandFilter("рандом "))
async def random_case(event: bot.SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:]).replace("<br>", "\n")
    print(message)
    new_message = ""
    for letter in message:
        if random.randint(0, 1) == 1:
            new_message += letter.upper()
        else:
            new_message += letter
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=new_message)


@bot.message_handler(CustomCommandFilter("бомба "))
async def bomb(event: bot.SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:])
    with open("config.json", "r") as f:
        content = loads(f.read())
        bomb_time = content["bomb_time"]
    if content["work_for_everyone"] is not True:
        bomb_id = event.object.object.message_id
    else:
        await event.answer("абоба")
        bomb_id = event.object.object.message_id+1

    for n in range(bomb_time, 0, -1):
        await edit_msg(api_session, bomb_id, event.peer_id,
                       text=f'{message}\n\nДанное сообщение взорвется через {n} секунд! &#128163;',)
        await asyncio.sleep(1.0)
    await edit_msg(api_session, bomb_id, event.peer_id,
                   text='БУМ! Взрывная беседа!! &#128165;&#128165;')
    await asyncio.sleep(3.0)
    await api_session.messages.delete(peer_id=event.peer_id,
                                      message_ids=bomb_id,
                                      delete_for_all=1)


@bot.message_handler(CustomCommandFilter("me "))
async def me(event: bot.SimpleBotEvent) -> str:
    action = ' '.join(event.object.object.text.split()[1:])
    who = await api_session.users.get(user_ids=event.object.object.message_data.from_id)
    name = who.response[0].first_name
    last_name = who.response[0].last_name
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=f'{name} {last_name} {action} &#128172;')


@bot.message_handler(CustomCommandFilter("бонкнуть"))
async def bonk(event: bot.SimpleBotEvent) -> str:
    conv_msg_id = loads(event.object.object.extra_message_data['reply'])['conversation_message_id']
    bonk_who = await api_session.messages.get_by_conversation_message_id(peer_id=event.peer_id, conversation_message_ids=conv_msg_id)
    bonk_who = bonk_who.response.items[0].from_id

    bonk_who_info = await api_session.users.get(user_ids=bonk_who, name_case="gen")
    bonk_who_name = bonk_who_info.response[0].first_name
    bonk_who_last_name = bonk_who_info.response[0].last_name

    who_bonks = await api_session.users.get(user_ids=event.object.object.message_data.from_id)
    name = who_bonks.response[0].first_name
    last_name = who_bonks.response[0].last_name
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=f'{name} {last_name} бонкнул {bonk_who_name} {bonk_who_last_name} &#129529;')


@bot.message_handler(CustomCommandFilter("бросить кактус"))
async def cactus(event: bot.SimpleBotEvent) -> str:
    conv_msg_id = loads(event.object.object.extra_message_data['reply'])['conversation_message_id']
    throw_to = await api_session.messages.get_by_conversation_message_id(peer_id=event.peer_id, conversation_message_ids=conv_msg_id)
    throw_to = throw_to.response.items[0].from_id

    throw_to_info = await api_session.users.get(user_ids=throw_to, name_case="gen")
    throw_to_name = throw_to_info.response[0].first_name
    throw_to_last_name = throw_to_info.response[0].last_name

    who_throws = await api_session.users.get(user_ids=event.object.object.message_data.from_id)
    name = who_throws.response[0].first_name
    last_name = who_throws.response[0].last_name
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   text=f'{name} {last_name} бросил кактус в {throw_to_name} {throw_to_last_name} &#127797;')


@bot.message_handler(CustomCommandFilter("дем "))
async def demotivator(event: bot.SimpleBotEvent) -> str:
    try:
        text = ' '.join(event.object.object.text.split()[1:])
        first_text = text.split("|")[0]
        second_text = text.split("|")[1]
        photo = await api_session.messages.get_by_id(message_ids=event.object.object.message_id)
        url = photo.response.items[0].attachments[0].photo.sizes[-1].url
        photo_bytes = requests.get(url).content
        with open("dem_output.png", "wb") as f:
            f.write(photo_bytes)

        # Создание демотиватора
        original = Image.open("Demotivator.png").convert('RGB')
        to_paste = Image.open("dem_output.png").convert('RGB')
        fnt = ImageFont.truetype("TNR.ttf", 70)
        fnt1 = ImageFont.truetype("TNR.ttf", 40)
        d = ImageDraw.Draw(original)

        original.paste(to_paste.resize((609, 517)), (75, 45))

        w, h = original.size
        W, H = d.textsize(first_text, font=fnt)
        W1, H1 = d.textsize(second_text, font=fnt1)

        d.text(((w-W)/2, 575), first_text, font=fnt, fill="white")
        d.text(((w-W1)/2, 650), second_text, font=fnt1, fill="white")
        original = original.save("DemotivatorFinal.png")

        # Отправка демотиватора
        attachment = await uploader.get_attachment_from_path(
            peer_id=event.peer_id,
            file_path="DemotivatorFinal.png"
        )
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                    attachment=attachment)
    except IndexError:
        await edit_msg(api_session, event.object.object.message_id,
                       event.peer_id, text="Вы не прикрепили фото к сообщению! "+error)


bot.run_forever()
