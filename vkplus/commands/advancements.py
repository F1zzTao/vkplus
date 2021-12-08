from vkbottle.tools import PhotoMessageUploader
from vkbottle.user import Blueprint, Message
from typing import Optional

from utils.edit_msg import edit_msg
from utils.emojis import error
from PIL import Image, ImageFont, ImageDraw, ImageOps
from os import getcwd, mkdir
from os.path import exists
import requests

bp = Blueprint("Advancements generator")


@bp.on.message(text="<prefix>ачивка <main_text>|<second_text>")
async def advancements(
    message: Message,
    main_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    if len(main_text) > 220 or len(second_text) > 220:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            "Вы не можете написать больше 220 символов " + error
        )
        return
    font = ImageFont.truetype(
        getcwd().replace("\\", "/") + "/minecraft-rus.ttf", 40
    )
    main_text_width = font.getsize(main_text)[0]
    second_text_width = font.getsize(second_text)[0]

    if not exists(getcwd().replace("\\", "/") + "/output/"):
        mkdir(getcwd().replace("\\", "/") + "/output/")

    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        photo_bytes = requests.get(url).content

        with open(
            getcwd().replace("\\", "/") + "/output/advancement_output.png",
            "wb",
        ) as f:
            f.write(photo_bytes)
        im4 = Image.open(
            getcwd().replace("\\", "/") + "/output/advancement_output.png"
        ).convert("RGBA")

    else:
        im4 = Image.open(
            getcwd().replace("\\", "/") + "/icon.png"
        ).convert("RGBA")

    im = Image.new(
        "RGBA",
        (
            main_text_width + 190
            if main_text_width+180 > second_text_width
            else second_text_width + 50,
            195,
        ),
    )
    im1 = Image.open(
        getcwd().replace("\\", "/") + "/AdvStart.png"
    ).convert("RGBA")
    im2 = Image.open(getcwd().replace("\\", "/") + "/AdvMiddle.png")
    im3 = Image.open(getcwd().replace("\\", "/") + "/AdvEnd.png")
    im4 = im4.resize((95, 90), Image.NEAREST)

    for i in range(0, im.width):
        im.paste(im2, (i, 0))

    im.paste(im1)
    im.paste(im3, (im.width - 10, 0))
    im.paste(im4, (40, 20), im4)
    d = ImageDraw.Draw(im)
    d.text((25, 135), second_text, font=font)
    d.text((170, 40), main_text, font=font)

    im = ImageOps.expand(im, border=100, fill="white")
    im.save(getcwd().replace("\\", "/") + "/output/temp.png")

    attachment = await PhotoMessageUploader(bp.api).upload(
        getcwd().replace("\\", "/") + "/output/temp.png",
        peer_id=message.peer_id
    )

    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        attachment=attachment,
    )
