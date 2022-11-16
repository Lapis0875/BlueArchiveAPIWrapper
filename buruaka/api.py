import asyncio
from functools import wraps
from pprint import pprint
from typing import Callable, Coroutine, Any, Tuple, Dict

import aiohttp

from buruaka.models.student import Student, StudentDetails
from buruaka.query import BuruakaQuery


def request(coro):
    @wraps(coro)
    async def wrapper(self: "BuruakaClient", *args, **kwargs):
        if self._session is None:
            await self.setup()
        return await coro(self, *args, **kwargs)
    return wrapper


class BuruakaClient:
    """
    BlueArchive Unofficial API Buruaka's API client.
    """

    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    async def setup(self):
        self._session = aiohttp.ClientSession(base_url="https://api.ennead.cc")

    async def get_chara(self, *, query: BuruakaQuery = None, chara: str = None) -> list[Student]:
        if query is not None:
            return await self.query_chara_details(query)
        if chara is not None:
            return [await self.single_chara(chara)]
        return await self.all_chara()

    @request    # i hate typing. damnit.
    async def query_chara(self, query: BuruakaQuery) -> list[str]:
        async with self._session.get(url="/buruaka/character" + query.build()) as resp:
            return await resp.json()

    @request
    async def query_chara_details(self, query: BuruakaQuery) -> list[StudentDetails]:
        chara_list = await self.query_chara(query)
        resp = await asyncio.gather(*map(
            lambda c: self.single_chara(c),
            chara_list
        ))
        pprint(resp)
        return resp

    @request
    async def single_chara(self, chara: str) -> StudentDetails:
        async with self._session.get(url=f"/buruaka/character/{chara}") as resp:
            json = await resp.json()
            pprint(json)
            return StudentDetails.from_json(json)

    @request
    async def all_chara(self) -> list[Student]:
        async with self._session.get(url="/buruaka/character") as resp:
            json = await resp.json()
            pprint(json)
            return list(map(Student.from_json, json["data"]))

    async def get_raid(self, query):
        pass

    async def close(self):
        await self._session.close()
        self._session = None

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
