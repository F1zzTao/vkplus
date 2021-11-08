from vkwave.bots import (
    simple_user_message_handler, DefaultRouter,
    SimpleBotEvent, PhotoUploader
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.emojis import error
from utils.apisession import api_session
import requests
from PIL import Image, ImageFont, ImageDraw
from os import getcwd

demotivator_router = DefaultRouter()
uploader = PhotoUploader(api_session)

@simple_user_message_handler(demotivator_router, CustomCommandFilter("дем "))
async def demotivator(event: SimpleBotEvent) -> str:
    text = ' '.join(event.object.object.text.split()[1:])
    if text.find("|") == -1:
        first_text = text
        second_text = ''
    else:
        first_text = text.split("|")[0]
        second_text = text.split("|")[1]

    photo = await api_session.messages.get_by_id(message_ids=event.object.object.message_id)
    try:
        url = photo.response.items[0].attachments[0].photo.sizes[-1].url
    except IndexError:
        await edit_msg(api_session, event.object.object.message_id,
                       event.peer_id, text="Вы не прикрепили фото к сообщению! "+error)
        return

    photo_bytes = requests.get(url).content
    with open(getcwd()+"/output/dem_output.png", "wb") as f:
        f.write(photo_bytes)

    # Создание демотиватора
    original = Image.open(getcwd()+"/Demotivator.png").convert('RGB')
    to_paste = Image.open(getcwd()+"/output/dem_output.png").convert('RGB')
    fnt = ImageFont.truetype(getcwd()+"/TNR.ttf", 70)
    fnt1 = ImageFont.truetype(getcwd()+"/TNR.ttf", 40)
    d = ImageDraw.Draw(original)

    original.paste(to_paste.resize((609, 517)), (75, 45))

    w, h = original.size
    W, H = d.textsize(first_text, font=fnt)
    W1, H1 = d.textsize(second_text, font=fnt1)

    d.text(((w-W)/2, 575), first_text, font=fnt, fill="white")
    d.text(((w-W1)/2, 650), second_text, font=fnt1, fill="white")
    original = original.save(getcwd()+"/output/DemotivatorFinal.png")

    # Отправка демотиватора
    attachment = await uploader.get_attachment_from_path(
        peer_id=event.peer_id,
        file_path=getcwd()+"/output/DemotivatorFinal.png"
    )
    await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                   attachment=attachment)