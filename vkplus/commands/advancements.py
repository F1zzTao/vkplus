from vkbottle.tools import PhotoMessageUploader
from vkbottle.user import Blueprint, Message
from typing import Optional

from utils.edit_msg import edit_msg
from utils.emojis import error
from filters import ForEveryoneRule
from PIL import Image, ImageFont, ImageDraw, ImageOps
import aiohttp

bp = Blueprint("Advancements generator")
path = "sources/advancements/"


@bp.on.message(
    ForEveryoneRule("advancements"),
    text="<prefix>ачивка <main_text>|<second_text>"
)
async def advancements(
    message: Message,
    main_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    if len(main_text) > 220 or len(second_text) > 220:
        await edit_msg(
            bp.api, message,
            "Вы не можете написать больше 220 символов " + error
        )
        return
    font = ImageFont.truetype(path + "minecraft-rus.ttf", 40)
    main_text_width = font.getsize(main_text)[0] + 180
    second_text_width = font.getsize(second_text)[0]

    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                photo_bytes = await resp.read()

        with open("output/adv_icon.png", "wb") as f:
            f.write(photo_bytes)
        adv_icon = Image.open("output/adv_icon.png").convert("RGBA")

    else:
        adv_icon = Image.open(path + "default.png").convert("RGBA")

    blank = Image.new(
        "RGBA",
        (
            main_text_width + 10
            if main_text_width > second_text_width
            else second_text_width + 50,
            195,
        ),
    )
    adv_start = Image.open(path + "adv_start.png").convert("RGBA")
    adv_middle = Image.open(path + "adv_middle.png")
    adv_end = Image.open(path + "adv_end.png")
    adv_icon = adv_icon.resize((95, 90), Image.NEAREST)

    for i in range(0, blank.width):
        blank.paste(adv_middle, (i, 0))

    blank.paste(adv_start)
    blank.paste(adv_end, (blank.width - 10, 0))
    blank.paste(adv_icon, (40, 20), adv_icon)
    d = ImageDraw.Draw(blank)
    d.text((25, 135), second_text, font=font)
    d.text((170, 40), main_text, font=font)

    blank = ImageOps.expand(blank, border=100, fill="white")
    blank.save("output/adv_final.png")

    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/adv_final.png", peer_id=message.peer_id
    )

    await edit_msg(
        bp.api, message,
        attachment=attachment,
    )
