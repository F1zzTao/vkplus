"""
Middleware that ckecks if user is the owner of the bot
"""
import json
from vkbottle import BaseMiddleware


# Мидлварь на проверку, является ли пользователь
# владельцем бота, или нет
class FromMeMiddleware(BaseMiddleware):
    """
    Middleware that ckecks if user is the owner of the bot
    """
    async def pre(self):
        with open("config.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        if not self.event.text.startswith(content["prefix"]):
            self.stop("Сообщение не начинается с префикса")
