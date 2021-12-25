import aiohttp


async def request(url, json=False):
    """
    Метод для отправки запросов
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if json:
                return await resp.json()
            return await resp.read()
