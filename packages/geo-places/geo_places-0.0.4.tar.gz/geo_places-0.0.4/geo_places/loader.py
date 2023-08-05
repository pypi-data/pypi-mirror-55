import asyncio
from typing import Generator, AsyncGenerator

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from geo_places.scraper import Scraper


def get_municipality_hrefs(bs: BeautifulSoup) -> Generator[str, None, None]:
    for a in bs.find_all("a"):
        yield a.get("href")


def names(bs: BeautifulSoup) -> Generator[str, None, None]:
    for tr in bs.find_all("tr"):
        for td in tr.find_all("td")[1::2]:
            yield td.text


async def get_names_with_gps():
    url = "https://wwwinfo.mfcr.cz/ares/obce/ares_obce.html.cz"
    async with MunicipalityLoader(url) as ml:
        muns = ml.municipality_names()
        tasks = [ml._scraper.get_gps(name) async for name in muns]
        return await asyncio.gather(*tasks, return_exceptions=True)


class MunicipalityLoader:
    def __init__(self, home_url: str) -> None:
        self.home_url = home_url
        self._session = ClientSession()
        self._scraper = Scraper(self._session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        if self._session:
            await self._session.close()

    async def municipality_pages(self) -> AsyncGenerator[str, None]:
        for s in await self._scraper.scrape(self.home_url, get_municipality_hrefs):
            yield urljoin(self.home_url, s)

    async def municipality_names(self) -> AsyncGenerator[str, None]:
        yielded = set()
        async for url in self.municipality_pages():
            for name in await self._scraper.scrape(url, names):
                if name not in yielded:
                    yield name
                    yielded.add(name)
