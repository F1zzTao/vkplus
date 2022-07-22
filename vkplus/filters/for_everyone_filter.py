import json
from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message


class ForEveryoneRule(ABCRule[Message]):
    def __init__(self, short_name: str):
        self.short_name = short_name

    async def check(self, event: Message) -> bool:
        with open("commands_settings.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        with open("config.json", "r", encoding="utf-8") as file:
            user_id = int(json.load(file)["user_id"])

        command = content[self.short_name]
        print(event.peer_id)
        if (
            event.from_id == user_id
            or command["allowed"] is True
            and event.peer_id not in command["blacklist"]
        ):
            return True
        return False
