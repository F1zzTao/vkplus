"""
Модуль для отправки запросов к апи
"""
import aiohttp


async def request(url):
    """
    Метод для отправки запросов к апи
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()
