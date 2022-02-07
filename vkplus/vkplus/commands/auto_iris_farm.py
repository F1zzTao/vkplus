from vkbottle.user import Blueprint
import time
import asyncio

bp = Blueprint("AutoIrisFarm")


async def main():
    while True:
        comment_id = await bp.api.wall.create_comment(
            owner_id=-174105461,
            post_id=6713149,
            message="ферма"
            )

        await bp.api.wall.delete_comment(
            owner_id=-174105461,
            comment_id=comment_id
        )

        time.sleep(14400)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
