\"\"\"Elasticsearch基础操作\"\"\"

from elasticsearch import Elasticsearch


def basic_operations():
    # 连接
    es = Elasticsearch(\"http://localhost:9200\")

    # 创建索引
    if not es.indices.exists(index=\"articles\"):
        es.indices.create(
            index=\"articles\",
            mappings={
                \"properties\": {
                    \"title\": {\"type\": \"text\", \"analyzer\": \"standard\"},
                    \"content\": {\"type\": \"text\"},
                    \"tags\": {\"type\": \"keyword\"},
                    \"author\": {\"type\": \"keyword\"},
                    \"created_at\": {\"type\": \"date\"},
                }
            },
            settings={
                \"number_of_shards\": 1,
                \"number_of_replicas\": 0,
            },
        )
        print(\"Index created\")

    # 索引文档
    docs = [
        {\"title\": \"Python Tutorial\", \"content\": \"Learn Python from scratch\", \"tags\": [\"python\", \"beginner\"], \"author\": \"Alice\"},
        {\"title\": \"Advanced Python\", \"content\": \"Deep dive into Python features\", \"tags\": [\"python\", \"advanced\"], \"author\": \"Bob\"},
        {\"title\": \"Web Development\", \"content\": \"Build web apps with Python and FastAPI\", \"tags\": [\"python\", \"web\"], \"author\": \"Alice\"},
    ]

    for i, doc in enumerate(docs, 1):
        es.index(index=\"articles\", id=i, document=doc)
    es.indices.refresh(index=\"articles\")
    print(f\"Indexed {len(docs)} documents\")

    # 搜索
    results = es.search(
        index=\"articles\",
        query={
            \"multi_match\": {
                \"query\": \"Python tutorial\",
                \"fields\": [\"title^2\", \"content\"],
            }
        },
    )

    print(f\"\\nSearch results ({results[\"hits\"][\"total\"][\"value\"]} hits):\"  )
    for hit in results[\"hits\"][\"hits\"]:
        print(f\"  {hit[\"_source\"][\"title\"]} (score: {hit[\"_score\"]:.2f})\")

    # 过滤
    results = es.search(
        index=\"articles\",
        query={
            \"bool\": {
                \"must\": [{\"match\": {\"content\": \"Python\"}}],
                \"filter\": [{\"term\": {\"author\": \"Alice\"}}],
            }
        },
    )
    print(f\"\\nFiltered results: {results[\"hits\"][\"total\"][\"value\"]} hits\")

    # 清理
    es.indices.delete(index=\"articles\")
    print(\"\\nIndex deleted\")


if __name__ == \"__main__\":
    basic_operations()
