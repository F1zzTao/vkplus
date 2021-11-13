from vkwave.bots import MiddlewareResult, BaseMiddleware, SimpleBotEvent
from json import loads
from os import getcwd

config_path = getcwd().replace("\\", "/") + "/config.json"


# Мидлварь на проверку, является ли пользователь
# пользователем, или же нет.
class FromMeMiddleware(BaseMiddleware):
    async def pre_process_event(
        self, event: SimpleBotEvent
    ) -> MiddlewareResult:
        if event.object.object.event_id == 4:
            with open(config_path, "r") as f:
                content = loads(f.read())
            if event.object.object.message_data.from_id == content["user_id"]:
                return MiddlewareResult(True)
            return MiddlewareResult(content["work_for_everyone"])
        return MiddlewareResult(False)
