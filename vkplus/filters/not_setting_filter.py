"""
Filter that prevents the commands "!info" and "!info dm" from collising
"""
from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message


class NotSettingRule(ABCRule[Message]):
    """
    Filter that prevents the commands "!info" and "!info dm" from collising
    """
    async def check(self, event: Message) -> bool:
        if len(event.text.split()) > 1:
            if event.text.split()[1] == "лс":
                return False
        return True
