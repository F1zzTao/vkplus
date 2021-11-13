from vkwave.bots.core.dispatching.filters.base import BaseFilter, FilterResult
from vkwave.bots import SimpleBotEvent
from json import loads
from os import getcwd

config_path = getcwd().replace("\\", "/") + "/config.json"


# Нормальный фильтр команд
class CustomCommandFilter(BaseFilter):
    def __init__(self, message) -> None:
        self.message = message
        with open(config_path, "r") as f:
            self.content = f.read()
            self.prefix = loads(self.content)["prefix"]

    async def check(self, event: SimpleBotEvent) -> FilterResult:
        text: str = event.object.object.text
        # я ненавижу pep8
        if text.startswith(self.prefix) and text[
            len(self.prefix):
        ].startswith(self.message):
            return FilterResult(True)
        return FilterResult(False)
