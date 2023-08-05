from elasticsearch_dsl import (
    Document,
    analyzer,
    GeoPoint,
    Integer,
    Keyword,
    Completion,
    Text,
)


LOCATION_INDEX_NAME = "location"


czech_analyzer = analyzer(
    "czech_analyzer", tokenizer="standard", filter=["lowercase", "asciifolding"]
)


class LocationDocument(Document):
    class Index:
        name = LOCATION_INDEX_NAME

    name = Text(analyzer=czech_analyzer, fields={"keyword": Keyword()})
    suggest = Completion(
        analyzer=czech_analyzer,
        contexts=[{"name": "country", "type": "category", "path": "country"}],
    )
    population = Integer()
    location = GeoPoint()
    country = Keyword()

    def clean(self):
        self.suggest = {
            "input": [self.name],
            "weight": self.population,
        }
