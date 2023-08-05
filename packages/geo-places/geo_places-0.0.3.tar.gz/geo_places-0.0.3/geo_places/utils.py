from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class Gps:
    lat: float
    lon: float

    @staticmethod
    def from_text(text: str) -> Gps:
        lat, lon = parse_gps(text)
        return Gps(lat, lon)


def parse_gps(content: str) -> tuple:
    regexp = r"/staticmap\?center=([0-9]+\.[0-9]*%2C[0-9]+\.[0-9]*)&amp"
    try:
        groups = re.search(regexp, content).groups()
        coordinates = groups[0].split("%2C")
        if len(coordinates) != 2:
            raise ValueError(f"invalid gps value: {groups}")
        return tuple(float(x) for x in coordinates)
    except IndexError:
        raise ValueError(f"does not contain valid GPS: {content}")
