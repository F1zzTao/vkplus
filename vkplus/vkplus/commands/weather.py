"""
Эта команда показывает прогноз погоды в
указанном городе используя openweathermap API
"""
from utils.edit_msg import edit_msg
from utils.emojis import ERROR
from utils.request_url import request
from filters import ForEveryoneRule

import json
from vkbottle.user import Blueprint, Message


bp = Blueprint("Weather output")


@bp.on.message(ForEveryoneRule("weather"), text="<prefix>погода <city>")
async def weather(message: Message, city):
    """
    > !погода Москва

    > 🏙 | Погода в Москве:
    > 🌡 | Температура: -17.51°C
    > 🧍 | Ощущается как: -24.01°C
    > ⬇ | Минимальная температура: -19.76°C
    > ⬆ | Максимальная температура: -15.98°C
    > 💧 | Влажность: 87%
    > 🌬 | Ветер: 2.65 м/с
    """

    with open("config.json", "r", encoding="utf-8") as file:
        owm_token = json.load(file)["owm_api_key"]
    if owm_token == "":
        await edit_msg(
            bp.api,
            message,
            f"{ERROR} | Вы не указали токен для openweathermap API!"
        )
        return

    owm_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={owm_token}"  # noqa: E501
    owm_response = await request(owm_url, True)

    if owm_response["cod"] == "404":
        await edit_msg(bp.api, message, f"{ERROR} | Город {city} не найден!")
        return

    main = owm_response["main"]
    wind = owm_response["wind"]

    await edit_msg(
        bp.api,
        message,
        f"&#127961; | Погода в {city}:\n"
        f"&#127777; | Температура: {main['temp']}°C\n"
        f"&#129485; | Ощущается как: {main['feels_like']}°C\n"
        f"&#11015; | Минимальная температура: {main['temp_min']}°C\n"
        f"&#11014; | Максимальная температура: {main['temp_max']}°C\n"
        f"&#128167; | Влажность: {main['humidity']}%\n"
        f"&#127788; | Ветер: {wind['speed']} м/с",
    )
