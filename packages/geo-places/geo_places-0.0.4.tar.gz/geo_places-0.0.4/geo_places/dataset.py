from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, AsyncGenerator

from geo_places.loader import get_names_with_gps
from geo_places.population import Population


@dataclass
class LocationObject:
    name: str
    population: int
    location: Dict[str, float]
    country: str

    @staticmethod
    def from_source(source: dict) -> LocationObject:
        return LocationObject(
            source.get("name"),
            source.get("population"),
            source.get("location"),
            source.get("country")
        )


async def gener_dataset(
    population_src: Path, country: str = "cz"
) -> AsyncGenerator[LocationObject, None]:
    places = await get_names_with_gps()
    with Population(population_src) as pop:
        for place in places:
            municipality, gps = place
            yield LocationObject(
                municipality, int(pop[municipality]), asdict(gps), country
            )
