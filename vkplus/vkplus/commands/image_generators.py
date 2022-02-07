from utils.edit_msg import edit_msg
from utils.emojis import ERROR
from utils.request_url import request
from filters import ForEveryoneRule

from typing import Optional
from PIL import Image, ImageFont, ImageDraw, ImageOps
from vkbottle.tools import PhotoMessageUploader
from vkbottle.user import Blueprint, Message


bp = Blueprint("Images generator")


# Advancements
ADV_PATH = "sources/advancements/"
ADV_FONT = ImageFont.truetype(ADV_PATH + "minecraft-rus.ttf", 40)

# Demotivators
DEM_PATH = "sources/demotivators/"
DEM_FONT = ImageFont.truetype(DEM_PATH + "TNR.ttf", 70)
DEM_FONT_SEC = ImageFont.truetype(DEM_PATH + "TNR.ttf", 40)

# Quotes
QUOTE_PATH = "sources/quotes/"
QUOTE_FONT = ImageFont.truetype(QUOTE_PATH + "Montserrat-Light.ttf", 70)
QUOTE_FONT_SEC = ImageFont.truetype(
    QUOTE_PATH + "Montserrat-MediumItalic.ttf", 70
)


@bp.on.message(
    ForEveryoneRule("advancements"),
    text="<prefix>ачивка <main_text>|<second_text>",
)
async def advancements(
    message: Message,
    main_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    """
    > !ачивка [текст1]|[текст2]
    """

    if len(main_text) > 220 or len(second_text) > 220:
        await edit_msg(
            bp.api,
            message,
            f"{ERROR} | Вы не можете написать больше 220 символов",
        )
        return
    main_text_width = ADV_FONT.getsize(main_text)[0] + 180
    second_text_width = ADV_FONT.getsize(second_text)[0]

    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        photo_bytes = await request(url)

        with open("output/adv_icon.png", "wb") as file:
            file.write(photo_bytes)
        adv_icon = Image.open("output/adv_icon.png").convert("RGBA")

    else:
        adv_icon = Image.open(ADV_PATH + "default_icon.png").convert("RGBA")

    blank = Image.new(
        "RGBA",
        (
            main_text_width + 10
            if main_text_width > second_text_width
            else second_text_width + 50,
            195,
        ),
    )
    adv_start = Image.open(ADV_PATH + "adv_start.png").convert("RGBA")
    adv_middle = Image.open(ADV_PATH + "adv_middle.png")
    adv_end = Image.open(ADV_PATH + "adv_end.png")
    adv_icon = adv_icon.resize((95, 90), Image.NEAREST)

    for i in range(blank.width):
        blank.paste(adv_middle, (i, 0))

    blank.paste(adv_start)
    blank.paste(adv_end, (blank.width - 10, 0))
    blank.paste(adv_icon, (40, 20), adv_icon)
    draw = ImageDraw.Draw(blank)
    draw.text((25, 135), second_text, font=ADV_FONT)
    draw.text((170, 40), main_text, font=ADV_FONT)

    # Adding white border to image
    blank = ImageOps.expand(blank, border=100, fill="white")

    # Saving and uploading image
    blank.save("output/adv_final.png")
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/adv_final.png", peer_id=message.peer_id
    )

    await edit_msg(
        bp.api,
        message,
        attachment=attachment,
    )


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
    """
    > !дем [текст1]|[текст2]
    > !дем [текст1]
    > !дем |[текст2]
    """

    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        photo_bytes = await request(url)

        with open("output/dem_output.png", "wb") as file:
            file.write(photo_bytes)
    else:
        await edit_msg(
            bp.api, message, f"{ERROR} | Вы не прикрепили фото к сообщению!"
        )
        return

    original = Image.open(DEM_PATH + "demotivator.png").convert("RGB")
    to_paste = Image.open("output/dem_output.png").convert("RGB")
    draw = ImageDraw.Draw(original)

    original.paste(to_paste.resize((609, 517)), (75, 45))

    photo_width = original.size[0]
    text_width = draw.textsize(first_text, font=DEM_FONT)[0]
    second_text_width = draw.textsize(second_text, font=DEM_FONT_SEC)[0]

    # First text
    draw.text(
        ((photo_width - text_width) / 2, 575),
        first_text,
        font=DEM_FONT,
        fill="white",
    )

    # Second text
    draw.text(
        ((photo_width - second_text_width) / 2, 650),
        second_text,
        font=DEM_FONT_SEC,
        fill="white",
    )

    # Saving and uploading image
    original.save("output/dem_final.png")
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/dem_final.png", peer_id=message.peer_id
    )
    await edit_msg(bp.api, message, attachment=attachment)


@bp.on.message(ForEveryoneRule("quote"), text="<prefix>цитата")
async def quote(message: Message):
    """
    > !цитата (ответ на сообщение)
    """

    if message.reply_message is None:
        await edit_msg(
            bp.api,
            message,
            f"{ERROR} | Вы не ответили на сообщение!",
        )
        return
    elif message.reply_message.text == "":
        await edit_msg(
            bp.api,
            message,
            f"{ERROR} | Сообщение пустое! (картинка, стикер?)",
        )
        return

    reply_text = "„"+message.reply_message.text+"“"
    reply_user_id = message.reply_message.from_id
    reply_response = await bp.api.users.get(
        user_ids=reply_user_id, fields="first_name,last_name"
    )

    author_name = (
        f"©{reply_response[0].first_name} {reply_response[0].last_name}"
    )
    reply_text_width = QUOTE_FONT.getsize_multiline(reply_text)[0]
    author_name_width = QUOTE_FONT.getsize_multiline(author_name)[0]

    if author_name_width > reply_text_width:
        width = author_name_width+70
    else:
        width = reply_text_width+310

    quote = Image.new("RGBA", (width + 400, 399), "#22212A")
    draw = ImageDraw.Draw(quote)
    width, height = quote.size

    author = await bp.api.users.get(reply_user_id, fields="photo_400_orig")
    author_photo_url = author[0].photo_400_orig
    author_photo = await request(author_photo_url)
    with open("output/quote_author.jpg", "wb") as file:
        file.write(author_photo)

    author_photo = Image.open("output/quote_author.jpg").convert("RGB")
    author_photo = author_photo.resize((350, 350), Image.ANTIALIAS)

    # Circle border around image
    background = Image.new("RGB", author_photo.size, "#22212A")
    mask = Image.new("L", author_photo.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse(
        (
            0,
            0,
            author_photo.size[0],
            author_photo.size[1],
        ),
        fill=255,
    )
    mask = Image.composite(author_photo, background, mask)

    quote.paste(mask, (25, 25))

    # Author name
    draw.text(
        (width - author_name_width - 30, height - 115),
        author_name,
        font=QUOTE_FONT,
        fill="white",
    )

    # Quote text
    draw.text(
        ((width+310-reply_text_width)/2, 140),
        reply_text,
        font=QUOTE_FONT_SEC,
        fill="white",
    )

    # Saving and uploading image
    quote.save("output/quote_final.png")
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/quote_final.png", peer_id=message.peer_id
    )
    await edit_msg(
        bp.api,
        message,
        attachment=attachment,
    )
