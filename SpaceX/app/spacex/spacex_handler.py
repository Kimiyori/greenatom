import json
from typing import Any
import aiohttp

URL = "https://spacex-production.up.railway.app/"


async def session_context(query: str) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            URL,
            json={"query": query},
        ) as response:
            data = await response.text()
            dict_data: dict[str, Any] = json.loads(data)
            return dict_data


async def get_data(query: str) -> dict[str, Any]:
    return await session_context(query)
