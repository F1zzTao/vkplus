import json
from vkbottle import BaseMiddleware


class FromMeMiddleware(BaseMiddleware):
    """
    Миддлварь, который проверяет, явялется ли пользователь
    владельцем бота, или же нет
    """
    async def pre(self):
        with open("config.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        if not self.event.text.startswith(content["prefix"]):
            self.stop("Сообщение не начинается с префикса")
