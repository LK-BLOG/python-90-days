\"\"\"搜索服务封装\"\"\"

from elasticsearch import Elasticsearch
from typing import Any


class SearchService:
    \"\"\"搜索引擎服务\"\"\"

    def __init__(self, es_url: str = \"http://localhost:9200\", index: str = \"articles\"):
        self.es = Elasticsearch(es_url)
        self.index = index

    def ensure_index(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(
                index=self.index,
                mappings={
                    \"properties\": {
                        \"title\": {\"type\": \"text\"},
                        \"content\": {\"type\": \"text\"},
                        \"tags\": {\"type\": \"keyword\"},
                        \"author\": {\"type\": \"keyword\"},
                    }
                },
            )

    def index_document(self, doc_id: str, document: dict) -> None:
        self.es.index(index=self.index, id=doc_id, document=document)

    def bulk_index(self, documents: list[dict]) -> None:
        actions = []
        for doc in documents:
            actions.append({\"index\": {\"_index\": self.index, \"_id\": doc[\"id\"]}})
            actions.append({k: v for k, v in doc.items() if k != \"id\"})
        self.es.bulk(operations=actions)
        self.es.indices.refresh(index=self.index)

    def search(
        self,
        query: str,
        filters: dict[str, Any] | None = None,
        page: int = 1,
        size: int = 20,
    ) -> dict:
        must = [{
            \"multi_match\": {
                \"query\": query,
                \"fields\": [\"title^2\", \"content\", \"tags\"],
            }
        }]

        body = {
            \"query\": {\"bool\": {\"must\": must}},
            \"from\": (page - 1) * size,
            \"size\": size,
            \"highlight\": {
                \"fields\": {
                    \"title\": {},
                    \"content\": {\"fragment_size\": 200, \"number_of_fragments\": 2},
                }
            },
        }

        if filters:
            body[\"query\"][\"bool\"][\"filter\"] = [{\"term\": {k: v}} for k, v in filters.items()]

        results = self.es.search(index=self.index, body=body)
        return {
            \"total\": results[\"hits\"][\"total\"][\"value\"],
            \"items\": [
                {
                    \"id\": hit[\"_id\"],
                    \"score\": hit[\"_score\"],
                    \"source\": hit[\"_source\"],
                    \"highlight\": hit.get(\"highlight\", {}),
                }
                for hit in results[\"hits\"][\"hits\"]
            ],
        }

    def delete_document(self, doc_id: str) -> None:
        self.es.delete(index=self.index, id=doc_id, ignore=[404])

    def suggest(self, prefix: str, size: int = 5) -> list[str]:
        body = {
            \"suggest\": {
                \"text\": prefix,
                \"title_suggest\": {
                    \"completion\": {\"field\": \"title.suggest\", \"size\": size},
                }
            }
        }
        results = self.es.search(index=self.index, body=body)
        return [
            opt[\"text\"] for opt in results.get(\"suggest\", {}).get(\"title_suggest\", [{}])[0].get(\"options\", [])
        ]
