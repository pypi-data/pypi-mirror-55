from __future__ import annotations

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import Callable, TypeVar, Optional, Tuple

from geo_places.utils import Gps

T = TypeVar("T")


def google_maps_url(search_query: str) -> str:
    query = "+".join(search_query.split(" "))
    return f"https://www.google.com/maps/search/ceska+republika+{query}"


class Scraper:
    def __init__(self, session: Optional[ClientSession] = None):
        if session:
            self._session = session
        else:
            self._session = ClientSession()

    async def __aenter__(self) -> Scraper:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.close()

    async def search_google_maps(self, query) -> str:
        async with self._session.get(google_maps_url(query)) as resp:
            resp.raise_for_status()
            return await resp.text()

    async def get_gps(self, query: str) -> Tuple[str, Gps]:
        return query, Gps.from_text(await self.search_google_maps(query))

    async def fetch(self, url: str) -> str:
        async with self._session.get(url) as resp:
            resp.raise_for_status()
            return await resp.text(encoding="latin2")

    async def scrape(self, url: str, func: Callable[[BeautifulSoup], T]) -> T:
        return func(BeautifulSoup(await self.fetch(url), features="html.parser"))
