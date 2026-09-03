# Day 65: RAG 基础

## 1. RAG是什么
用户问题 -> 向量化 -> 搜索相似片段 -> 拼接上下文 -> LLM生成答案

## 2. 分块策略
- 固定大小分块（带重叠）
- 按句子/段落分块
- chunk_size: 200-1000 tokens

## 3. 向量嵌入
将文本转为数值向量，语义相似则向量距离近。

## 4. 语义搜索
```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

## 5. 完整流程
分块 -> 嵌入 -> 存储 -> 查询时搜索+生成
