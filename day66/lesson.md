# Day 66: 向量数据库

## 1. 概念
专门存储和检索高维向量的数据库。支持ANN(近似最近邻)搜索。

## 2. 主流选择
- ChromaDB: 轻量本地, Python友好, 适合原型
- FAISS: Facebook出品, 超大规模, 需自己管理
- Pinecone: 全托管云服务, 适合生产

## 3. ChromaDB基础操作
```python
import chromadb
client = chromadb.Client()
col = client.create_collection("my_docs")
col.add(documents=["text1","text2"], ids=["1","2"])
results = col.query(query_texts=["问题"], n_results=3)
```

## 4. 索引类型
- Flat: 精确搜索, 小数据集
- IVF: 倒排索引, 中等规模
- HNSW: 层次图, 大规模高性能

## 5. 选型建议
小型原型 -> ChromaDB | 大规模本地 -> FAISS | 生产云 -> Pinecone/Weaviate
