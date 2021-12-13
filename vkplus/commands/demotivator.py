from vkbottle.tools import PhotoMessageUploader
from vkbottle.bot import Blueprint, Message

from typing import Optional
from utils.edit_msg import edit_msg
from utils.emojis import error
from filters import ForEveryoneRule
import aiohttp
from PIL import Image, ImageFont, ImageDraw


bp = Blueprint("Demotivator generator")
path = "sources/demotivator/"


@bp.on.message(
    ForEveryoneRule("demotivator"),
    text=[
        "<prefix>дем <first_text>|<second_text>",
        "<prefix>дем <first_text>",
        "<prefix>дем |<second_text>",
    ],
)
async def demotivator(
    message: Message,
    first_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                photo_bytes = await resp.read()

        with open("output/dem_output.png", "wb") as f:
            f.write(photo_bytes)
    else:
        await edit_msg(
            bp.api, message, f"{error} | Вы не прикрепили фото к сообщению! "
        )
        return

    # Создание демотиватора
    original = Image.open(path + "dem.png").convert("RGB")
    to_paste = Image.open("output/dem_output.png").convert("RGB")
    fnt = ImageFont.truetype(path + "TNR.ttf", 70)
    fnt1 = ImageFont.truetype(path + "TNR.ttf", 40)
    draw = ImageDraw.Draw(original)

    original.paste(to_paste.resize((609, 517)), (75, 45))

    photo_width = original.size[0]
    text_width = draw.textsize(first_text, font=fnt)[0]
    second_text_width = draw.textsize(second_text, font=fnt1)[0]

    draw.text(
        ((photo_width - text_width) / 2, 575),
        first_text,
        font=fnt,
        fill="white",
    )
    draw.text(
        ((photo_width - second_text_width) / 2, 650),
        second_text,
        font=fnt1,
        fill="white",
    )
    original = original.save("output/dem_final.png")

    # Отправка демотиватора
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/dem_final.png", peer_id=message.peer_id
    )

    await edit_msg(bp.api, message, attachment=attachment)
