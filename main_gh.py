import asyncio
from vkwave.bots import (
    SimpleLongPollUserBot,
    MiddlewareResult, BotEvent,
    create_api_session_aiohttp,
    PhotoUploader)
from PIL import Image, ImageDraw, ImageFont
from json import loads
import random
import re
import requests

defaultConfig = '{\n    "token": "",\n    "id": ""\n}'

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
prefix = "!"
work_for_everyone = False
bomb_time = 10


# Мидлварь на проверку, является ли пользователь
# пользователем, или же нет.
@bot.middleware()
async def fromme(event: BotEvent) -> MiddlewareResult:
    if event.object.object.event_id == 4:
        if event.object.object.message_data.from_id == user_id:
            return MiddlewareResult(True)
        return MiddlewareResult(work_for_everyone)
    return False


# Настройки
@bot.message_handler(bot.text_filter(prefix+"для всех"))
async def for_everyone(event: bot.SimpleBotEvent) -> str:
    global work_for_everyone
    if work_for_everyone is False:
        work_for_everyone = True
        await event.answer("Команды для всех включены")
    else:
        work_for_everyone = False
        await event.answer("Команды для всех выключены")


@bot.message_handler(bot.text_startswith_filter(prefix+"время бомбы "))
async def set_bomb_time(event: bot.SimpleBotEvent) -> str:
    time = int(event.object.object.text.split()[2])
    if time < 1:
        await event.answer(f"Время бомбы не может быть меньше 1!")
    else:
        global bomb_time
        bomb_time = time
        await event.answer(f"Время бомбы изменено на {bomb_time}")


@bot.message_handler(bot.text_startswith_filter(prefix+"время бомбы "))
async def set_prefix(event: bot.SimpleBotEvent) -> str:
    time = int(event.object.object.text.split()[2])
    if time < 1:
        await event.answer(f"Время бомбы не может быть меньше 1!")
    else:
        global bomb_time
        bomb_time = time
        await event.answer(f"Время бомбы изменено на {bomb_time}")


# Команды
@bot.message_handler(bot.text_startswith_filter(prefix+"пустое "))
async def empty_message(event: bot.SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:])
    text = re.sub("\w", "&#10240;", message)
    await event.answer(text)


@bot.message_handler(bot.text_startswith_filter(prefix+"рандом "))
async def random_case(event: bot.SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:])
    new_message = ""
    for letter in message:
        if random.randint(0, 1) == 1:
            new_message += letter.upper()
        else:
            new_message += letter
    await event.answer(new_message)


@bot.message_handler(bot.text_startswith_filter(prefix+"бомба "))
async def bomb(event: bot.SimpleBotEvent) -> str:
    message = ' '.join(event.object.object.text.split()[1:])
    for n in range(bomb_time, 0, -1):
        print("bomb"+str(n))
        await api_session.messages.edit(peer_id=event.peer_id,
                                        message=f'{message}\n\nДанное сообщение взорвется через {n} секунд!',
                                        message_id=event.object.object.message_id)
        await asyncio.sleep(1.0)
    await api_session.messages.edit(peer_id=event.peer_id,
                                    message=f'&#128165;&#128165; БУМ! Взрывная беседа!! &#128165;&#128165;',
                                    message_id=event.object.object.message_id)
    await asyncio.sleep(3.0)
    await api_session.messages.delete(peer_id=event.peer_id,
                                      message_ids=event.object.object.message_id,
                                      delete_for_all=1)


@bot.message_handler(bot.text_startswith_filter(prefix+"me "))
async def me(event: bot.SimpleBotEvent) -> str:
    action = ' '.join(event.object.object.text.split()[1:])
    who = await api_session.users.get(user_ids=event.object.object.message_data.from_id)
    name = who.response[0].first_name
    last_name = who.response[0].last_name
    await event.answer(f"{name} {last_name} {action}")
    
    
@bot.message_handler(bot.text_startswith_filter(prefix+"бонкнуть "))
async def bonk(event: bot.SimpleBotEvent) -> str:
    who = ' '.join(event.object.object.text.split()[1:])
    who_bonked = await api_session.users.get(user_ids=event.object.object.message_data.from_id)
    name = who_bonked.response[0].first_name
    last_name = who_bonked.response[0].last_name
    await event.answer(f"{name} {last_name} бонкнул {who}")
    
    
@bot.message_handler(bot.text_startswith_filter(prefix+"дем "))
async def demotivator(event: bot.SimpleBotEvent) -> str:
    text = ' '.join(event.object.object.text.split()[1:])
    first_text = text.split("|")[0]
    second_text = text.split("|")[1]
    photo = await api_session.messages.get_by_id(message_ids=event.object.object.message_id)
    url = photo.response.items[0].attachments[0].photo.sizes[-1].url
    photo_bytes = requests.get(url).content
    with open("dem_output.png","wb") as f:
        f.write(photo_bytes)
        
    # Создание демотиватора
    original = Image.open("Demotivator.png").convert('RGB')
    to_paste = Image.open("dem_output.png").convert('RGB')
    fnt = ImageFont.truetype("TNR.ttf",70)
    fnt1 = ImageFont.truetype("TNR.ttf",40)
    d = ImageDraw.Draw(original)
    d_paste = ImageDraw.Draw(to_paste)
        
    original.paste(to_paste.resize((609,517)),(75,45))

    w,h = original.size
    W,H = d.textsize(first_text,font=fnt)
    W1,H1 = d.textsize(second_text,font=fnt1)
    
    d.text(((w-W)/2,575),first_text,font=fnt,fill="white")
    d.text(((w-W1)/2,650),second_text,font=fnt1,fill="white")
    original = original.save("DemotivatorFinal.png")
    
    attachment = await uploader.get_attachment_from_path(
        peer_id = event.peer_id,
        file_path = "DemotivatorFinal.png"
    )
    await api_session.messages.send(peer_id=event.peer_id,
                                    attachment=attachment,
                                    random_id=0)


bot.run_forever()
