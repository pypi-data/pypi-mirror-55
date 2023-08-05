import asyncio
from pathlib import Path

from geo_places.dataset import gener_dataset
from geo_places.elasticsearch.handler import ElasticClient


url = "https://wwwinfo.mfcr.cz/ares/obce/ares_obce.html.cz"

# this is a default path where the data file lands after package installation
path = Path("../data/municipality_population.csv")


async def populate():
    es = ElasticClient("https://4366t46145t3:as36df42354-++-+-13+-4@es-test.usevoice-cicd.eu:443", use_ssl=True)
    await es.index_location_objects(gener_dataset(path))


def main():
    asyncio.run(populate())


if __name__ == '__main__':
    main()
