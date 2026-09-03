# Day 56 课程：搜索引擎

## 第一部分：全文搜索概念

### 1.1 倒排索引
`
文档1: "Python is great"
文档2: "Python is easy"
文档3: "Java is fast"

倒排索引:
  "Python" → [doc1, doc2]
  "is"     → [doc1, doc2, doc3]
  "great"  → [doc1]
  "easy"   → [doc2]
  "Java"   → [doc3]
  "fast"   → [doc3]
`

### 1.2 搜索相关性评分
- TF-IDF：词频 × 逆文档频率
- BM25：改进的TF-IDF

---

## 第二部分：Elasticsearch基础

### 2.1 安装和配置
`ash
# Docker启动
docker run -d --name es -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.12.0

# Python客户端
pip install elasticsearch
`

### 2.2 基本操作
`python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# 创建索引
es.indices.create(index="articles", mappings={
    "properties": {
        "title": {"type": "text", "analyzer": "standard"},
        "content": {"type": "text"},
        "tags": {"type": "keyword"},
        "created_at": {"type": "date"},
    }
})

# 索引文档
es.index(index="articles", id=1, document={
    "title": "Python Tutorial",
    "content": "Learn Python programming",
    "tags": ["python", "tutorial"],
})

# 搜索
results = es.search(index="articles", query={
    "multi_match": {
        "query": "Python programming",
        "fields": ["title^2", "content"]
    }
})
`

---

## 第三部分：Python搜索集成

### 3.1 搜索服务封装
`python
class SearchService:
    def __init__(self, es: Elasticsearch, index: str):
        self.es = es
        self.index = index

    async def index_document(self, id: str, doc: dict):
        await self.es.index(index=self.index, id=id, document=doc)

    async def search(self, query: str, filters: dict = None, page: int = 1, size: int = 20):
        must = [{"multi_match": {"query": query, "fields": ["title^2", "content"]}}]
        if filters:
            must.append({"term": filters})

        body = {
            "query": {"bool": {"must": must}},
            "from": (page - 1) * size,
            "size": size,
            "highlight": {
                "fields": {"title": {}, "content": {"fragment_size": 200}}
            }
        }
        return await self.es.search(index=self.index, body=body)

    async def delete_document(self, id: str):
        await self.es.delete(index=self.index, id=id)
`

---

## 本课总结

| 概念 | 说明 |
|------|------|
| 倒排索引 | 词→文档映射 |
| BM25 | 相关性评分算法 |
| Elasticsearch | 分布式搜索/分析引擎 |
| highlight | 搜索结果高亮 |
| analyzer | 分词器 |
