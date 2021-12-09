from vkbottle.tools import PhotoMessageUploader
from vkbottle.bot import Blueprint, Message

from typing import Optional
from utils.edit_msg import edit_msg
from utils.emojis import error
import requests
from PIL import Image, ImageFont, ImageDraw


bp = Blueprint("Demotivator generator")


@bp.on.message(
    text=[
        "<prefix>дем <first_text>|<second_text>",
        "<prefix>дем <first_text>",
        "<prefix>дем |<second_text>",
    ]
)
async def demotivator(
    message: Message,
    first_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    try:
        url = message.attachments[0].photo.sizes[-1].url
    except IndexError:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Вы не прикрепили фото к сообщению! " + error,
        )
        return

    photo_bytes = requests.get(url).content
    with open("output/dem_output.png", "wb") as f:
        f.write(photo_bytes)

    # Создание демотиватора
    original = Image.open("Demotivator.png").convert("RGB")
    to_paste = Image.open("output/dem_output.png").convert("RGB")
    fnt = ImageFont.truetype("TNR.ttf", 70)
    fnt1 = ImageFont.truetype("TNR.ttf", 40)
    d = ImageDraw.Draw(original)

    original.paste(to_paste.resize((609, 517)), (75, 45))

    w, h = original.size
    W, H = d.textsize(first_text, font=fnt)
    W1, H1 = d.textsize(second_text, font=fnt1)

    d.text(((w - W) / 2, 575), first_text, font=fnt, fill="white")
    d.text(((w - W1) / 2, 650), second_text, font=fnt1, fill="white")
    original = original.save("output/DemotivatorFinal.png")

    # Отправка демотиватора
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/DemotivatorFinal.png",
        peer_id=message.peer_id
    )

    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        attachment=attachment,
    )
