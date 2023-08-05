from typing import Type, Union, AsyncGenerator, List, Optional
from dataclasses import asdict

import certifi
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document

from geo_places.dataset import LocationObject
from geo_places.elasticsearch.documents import LocationDocument, LOCATION_INDEX_NAME


class ElasticClient:
    def __init__(
        self,
        host: Optional[str] = None,
        client: Optional[Elasticsearch] = None,
        use_ssl: bool = False,
        ca_certs: str = certifi.where(),
    ) -> None:
        if host:
            self.host = host
        if client:
            self._client = client
        else:
            if not host:
                raise ValueError(
                    "either 'client' or 'host' parameter must be provided!"
                )
            self._client = Elasticsearch(
                hosts=host, use_ssl=use_ssl, ca_certs=ca_certs if use_ssl else None
            )

    def create_index(self, document: Union[Type[Document], Document]) -> None:
        document.init(using=self._client)

    async def index_location_objects(
        self, source_objects: AsyncGenerator[LocationObject, None]
    ):
        self.create_index(LocationDocument)
        async for obj in source_objects:
            LocationDocument(**asdict(obj)).save(using=self._client)

    def search_location(
        self, query: str, country: str = "cz", size: int = 10, fuzzy: bool = False
    ) -> List[LocationObject]:
        body = {
            "size": size,
            "query": {
                "bool": {
                    "filter": {"term": {"country": country}},
                    "must": [
                        {
                            "match": {
                                "name": {
                                    "query": query,
                                    "fuzziness": "AUTO" if fuzzy else 0,
                                }
                            }
                        }
                    ],
                }
            },
        }
        res = self._client.search(body=body, index=LOCATION_INDEX_NAME)
        return [
            LocationObject.from_source(doc.get("_source", {}))
            for doc in res.get("hits", {}).get("hits", [])
        ]

    def suggest_location(
        self, query: str, country: str = "cz", size: int = 10, fuzzy: bool = False
    ) -> List[LocationObject]:
        body = {
            "size": 0,
            "suggest": {
                "locations": {
                    "text": query,
                    "completion": {
                        "field": "suggest",
                        "fuzzy": fuzzy,
                        "size": size,
                        "contexts": {"country": country},
                    },
                }
            },
        }
        res = self._client.search(body=body, index=LOCATION_INDEX_NAME)
        try:
            return [
                LocationObject.from_source(doc.get("_source", {}))
                for doc in res.get("suggest", {})
                .get("locations", [])[0]
                .get("options", [])
            ]
        except IndexError:
            return []
