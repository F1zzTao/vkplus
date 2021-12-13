from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message


class NotSettingRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        if len(event.text.split()) > 1:
            if event.text.split()[1] == "лс":
                return False
        return True
