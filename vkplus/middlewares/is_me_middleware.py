from vkbottle import BaseMiddleware
from json import loads
from os import getcwd


# Мидлварь на проверку, является ли пользователь
# владельцем бота, или нет
class FromMeMiddleware(BaseMiddleware):
    async def pre(self):
        config_path = getcwd().replace("\\", "/") + "/config.json"
        with open(config_path, "r") as f:
            content = loads(f.read())
        if not self.event.text.startswith(content["prefix"]):
            self.stop("Сообщение не начинается с префикса")
        if (
            int(self.event.from_id) != int(content["user_id"])
            and content["work_for_everyone"] is False
        ):
            print(self.event.from_id)
            print(content["user_id"])
            print(content["work_for_everyone"])
            self.stop("Сообщение было прислано не от владельца")
