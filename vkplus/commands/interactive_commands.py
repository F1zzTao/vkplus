"""
Roleplay-команды (!me, !бросить кактус и т. д.)
"""
from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from utils.emojis import ERROR
from filters import ForEveryoneRule

bp = Blueprint("Interactive commands")


class Interactive:
    """
    Класс, который возвращает имена людей
    """
    def __init__(
        self, api, message: Message, split_to: int, name_case: str = "acc"
    ):
        self.api = api
        self.message = message
        self.split_to = split_to
        self.name_case = name_case

    async def get_my_name(self) -> str:
        response = await self.api.users.get(
            user_ids=self.message.from_id, fields="first_name,last_name"
        )
        return (  # Тимур Богданов
            f"{response[0].first_name} {response[0].last_name}"
        )

    async def get_target_name(self) -> str:
        if len(self.message.text.split()) > self.split_to:
            mention = self.message.text.split()[self.split_to]
            if mention.startswith("["):
                who = mention.split("|")[0][1:].replace(
                    "id", ""
                )  # [id322615766|Тимур Богданов] -> 322615766
                response = await self.api.users.get(
                    user_ids=who,
                    fields="first_name,last_name",
                    name_case=self.name_case,
                )
                return (  # 322615766 -> [id322615766|Тимур Богданов]
                    "[id"
                    f"{who}|{response[0].first_name} {response[0].last_name}"
                    "]"
                )

            else:
                await edit_msg(
                    bp.api,
                    self.message,
                    text=(
                        f"{ERROR} | Вы написали не упоминание, а какую ту"
                        " чушь!"
                    )
                )

        elif self.message.reply_message is not None:
            who = self.message.reply_message.from_id
            response = await self.api.users.get(
                user_ids=who,
                fields="first_name,last_name",
                name_case=self.name_case,
            )
            return (  # 322615766 -> [id322615766|Тимур Богданов]
                f"[id{who}|{response[0].first_name} {response[0].last_name}]"
            )

        else:
            await edit_msg(
                bp.api,
                self.message,
                text=f"{ERROR} | Вы не ответили никому!",
            )
        return


"""
> !me съел суши
> Тимур Богданов съел суши 💬
"""


@bp.on.message(
    ForEveryoneRule("interactive_commands"), text="<prefix>me <action>"
)
async def me_handler(message: Message, action):
    who = await bp.api.users.get(user_ids=message.from_id)
    name = who[0].first_name
    last_name = who[0].last_name
    await edit_msg(
        bp.api, message, text=f"{name} {last_name} {action} &#128172;"
    )


"""
> !бонкнуть @vcirnik
> Тимур Богданов бонкнул Влада Сырника 🧹
"""


@bp.on.message(
    ForEveryoneRule("interactive_commands"),
    text=["<prefix>бонкнуть", "<prefix>бонкнуть <mention>"],
)
async def bonk_handler(message: Message):
    interactive = Interactive(bp.api, message, 1)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} бонкнул "
            f"{await interactive.get_target_name()} &#129529;"
        )
    )


"""
> !бросить кактус @vcirnik
> Тимур Богданов бросил кактус в Влада Сырника 🌵
"""


@bp.on.message(
    ForEveryoneRule("interactive_commands"),
    text=["<prefix>бросить кактус", "<prefix>бросить кактус <mention>"],
)
async def cactus_handler(message: Message):
    interactive = Interactive(bp.api, message, 2)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} бросил кактус в "
            f"{await interactive.get_target_name()} &#127797;"
        )
    )
