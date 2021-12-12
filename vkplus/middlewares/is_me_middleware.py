from vkbottle import BaseMiddleware
import json


# Мидлварь на проверку, является ли пользователь
# владельцем бота, или нет
class FromMeMiddleware(BaseMiddleware):
    async def pre(self):
        with open("config.json", "r") as f:
            content = json.loads(f.read())
        if not self.event.text.startswith(content["prefix"]):
            self.stop("Сообщение не начинается с префикса")
        if (
            int(self.event.from_id) != int(content["user_id"])
            and content["work_for_everyone"] is False
        ):
            self.stop("Сообщение было прислано не от владельца")
