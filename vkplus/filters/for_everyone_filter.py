from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message
import json


class ForEveryoneRule(ABCRule[Message]):
    def __init__(self, short_name: str):
        self.short_name = short_name

    async def check(self, event: Message) -> bool:
        with open("commands_for_everyone.json", "r") as f:
            content = json.load(f)
        with open("config.json", "r") as f:
            user_id = int(json.load(f)["user_id"])
        if content[self.short_name] or event.from_id == user_id:
            return True
        return False
