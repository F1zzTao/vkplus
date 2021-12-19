"""
Команда, которая генерирует достижение в стиле Minecraft
"""
from typing import Optional
from PIL import Image, ImageFont, ImageDraw, ImageOps

from vkbottle.tools import PhotoMessageUploader
from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from utils.emojis import ERROR
from utils.request_url import request
from filters import ForEveryoneRule


bp = Blueprint("Advancements generator")
PATH = "sources/advancements/"
FONT = ImageFont.truetype(PATH + "minecraft-rus.ttf", 40)


@bp.on.message(
    ForEveryoneRule("advancements"),
    text="<prefix>ачивка <main_text>|<second_text>"
)
async def advancements(
    message: Message,
    main_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    """
    > !ачивка [текст1]|[текст2]
    """
    # pylint: disable=too-many-locals
    if len(main_text) > 220 or len(second_text) > 220:
        await edit_msg(
            bp.api, message,
            f"{ERROR} | Вы не можете написать больше 220 символов"
        )
        return
    main_text_width = FONT.getsize(main_text)[0] + 180
    second_text_width = FONT.getsize(second_text)[0]


    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        photo_bytes = await request(url)

        with open("output/adv_icon.png", "wb") as file:
            file.write(photo_bytes)
        adv_icon = Image.open("output/adv_icon.png").convert("RGBA")

    else:
        adv_icon = Image.open(PATH + "default_icon.png").convert("RGBA")

    blank = Image.new(
        "RGBA",
        (
            main_text_width + 10
            if main_text_width > second_text_width
            else second_text_width + 50,
            195,
        ),
    )
    adv_start = Image.open(PATH + "adv_start.png").convert("RGBA")
    adv_middle = Image.open(PATH + "adv_middle.png")
    adv_end = Image.open(PATH + "adv_end.png")
    adv_icon = adv_icon.resize((95, 90), Image.NEAREST)

    for i in range(0, blank.width):
        blank.paste(adv_middle, (i, 0))

    blank.paste(adv_start)
    blank.paste(adv_end, (blank.width - 10, 0))
    blank.paste(adv_icon, (40, 20), adv_icon)
    draw = ImageDraw.Draw(blank)
    draw.text((25, 135), second_text, font=FONT)
    draw.text((170, 40), main_text, font=FONT)

    blank = ImageOps.expand(blank, border=100, fill="white")
    blank.save("output/adv_final.png")

    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/adv_final.png", peer_id=message.peer_id
    )

    await edit_msg(
        bp.api, message,
        attachment=attachment,
    )
