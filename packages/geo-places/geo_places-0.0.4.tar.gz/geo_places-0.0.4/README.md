# geo locations
A simple package for managing czech municipalities. It enables to scrape source data (czech municipalities together with their GPS coordinates), store them into ES index and then make queries.

## Installation
### Using pip
``pip3 install geo-places``

## Directly from github
``pip3 install git+https://github.com/bauerji/geo_locations.git``

## Usage
### Location index preparation
```python
import asyncio
from pathlib import Path

from geo_places.dataset import gener_dataset
from geo_places.elasticsearch.handler import ElasticClient


url = "https://wwwinfo.mfcr.cz/ares/obce/ares_obce.html.cz"

# this is a default path where the data file lands after package installation
path = Path("/usr/local/data/municipality_population.csv")


async def populate():
    es = ElasticClient("localhost")
    await es.index_location_objects(gener_dataset(path))


def main():
    asyncio.run(populate())


if __name__ == '__main__':
    main()
```

### Location suggest
```python
from geo_places.elasticsearch.handler import ElasticClient


if __name__ == '__main__':
    es = ElasticClient("localhost")
    suggestions = es.suggest_location("hor")
    for suggestion in suggestions:
        print(suggestion.name, suggestion.population)
```

### Location search
```python
from geo_places.elasticsearch.handler import ElasticClient


if __name__ == '__main__':
    es = ElasticClient("localhost")
    results = es.search_location("prha 10", fuzzy=True)
    for result in results:
        print(result)
```

## TODOs:
- tests
