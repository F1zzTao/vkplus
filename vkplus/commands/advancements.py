from vkwave.bots import (
    simple_user_message_handler, DefaultRouter,
    SimpleBotEvent, PhotoUploader
)
from filters.filters import CustomCommandFilter
from utils.edit_msg import edit_msg
from utils.apisession import api_session
from utils.emojis import error
from PIL import Image, ImageFont, ImageDraw, ImageOps
from os import getcwd
import requests

advancements_router = DefaultRouter()
uploader = PhotoUploader(api_session)

@simple_user_message_handler(advancements_router, CustomCommandFilter("ачивка "))
async def advancements(event: SimpleBotEvent):
    text = ' '.join(event.object.object.text.split()[1:])
    if len(text.split("|")) > 1:
        main_text = text.split("|")[0]
        second_text = text.split("|")[1]
        if len(main_text) > 220 or len(second_text) > 220:
            await event.answer('Вы не можете написать больше 220 символов '+error)
            return

        font = ImageFont.truetype(getcwd()+"/minecraft-rus.ttf",40)
        main_text_width = font.getsize(main_text)[0]+25
        second_text_width = font.getsize(second_text)[0]

        photo = await api_session.messages.get_by_id(message_ids=event.object.object.message_id)
        try:
            url = photo.response.items[0].attachments[0].photo.sizes[-1].url
            photo_bytes = requests.get(url).content
            with open(getcwd()+"/output/advancement_output.png", "wb") as f:
                f.write(photo_bytes)
            im4 = Image.open(getcwd()+"/output/advancement_output.png").convert("RGBA")
        except IndexError:
            im4 = Image.open(getcwd()+"/icon.png").convert("RGBA")

        im = Image.new("RGBA",(main_text_width+165 if main_text_width > second_text_width else second_text_width+50,195))
        im1 = Image.open(getcwd()+"/AdvStart.png").convert("RGBA")
        im2 = Image.open(getcwd()+"/AdvMiddle.png")
        im3 = Image.open(getcwd()+"/AdvEnd.png")
        im4 = im4.resize((95,90),Image.NEAREST)

        for i in range(0,im.width):
            im.paste(im2,(i,0))

        im.paste(im1)
        im.paste(im3,(im.width-10,0))
        im.paste(im4,(40,20),im4)
        d = ImageDraw.Draw(im)
        d.text((25,135),second_text,font=font)
        d.text((170,40),main_text,font=font)

        im = ImageOps.expand(im, border=100, fill="white")
        im.save(getcwd()+"/output/temp.png")

        attachment = await uploader.get_attachment_from_path(
            peer_id=event.peer_id,
            file_path=getcwd()+"/output/temp.png"
        )
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       attachment=attachment)
    else:
        await edit_msg(api_session, event.object.object.message_id, event.peer_id,
                       text="Вы не написали второй текст! "+error)
