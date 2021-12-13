from vkbottle import BaseMiddleware
import json


# Мидлварь на проверку, является ли пользователь
# владельцем бота, или нет
class FromMeMiddleware(BaseMiddleware):
    async def pre(self):
        with open("config.json", "r") as f:
            content = json.load(f)
        if not self.event.text.startswith(content["prefix"]):
            self.stop("Сообщение не начинается с префикса")
