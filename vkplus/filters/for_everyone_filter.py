import json
from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message


class ForEveryoneRule(ABCRule[Message]):
    """
    Фильтр для проверки, может ли пользователь использовать команду
    """
    def __init__(self, short_name: str):
        self.short_name = short_name

    async def check(self, event: Message) -> bool:
        with open("commands_for_everyone.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        with open("config.json", "r", encoding="utf-8") as file:
            user_id = int(json.load(file)["user_id"])
        if content[self.short_name] or event.from_id == user_id:
            return True
        return False
