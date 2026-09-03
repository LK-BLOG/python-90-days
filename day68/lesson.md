# Day 68: RAG 进阶

## 1. Query Rewriting
改写用户问题以提高检索质量。
例: "Python怎么学?" -> "Python编程语言 学习路线 入门教程"

## 2. HyDE
先让LLM生成假设答案, 用假设答案做检索(假设答案和文档更相似)。

## 3. Self-RAG
LLM自己判断: 需要检索吗? 检索结果有用吗? 答案有依据吗?

## 4. Reranking
用交叉编码器对初步检索结果重新打分排序。

## 5. RAG评估(Ragas)
- Faithfulness: 答案是否忠于检索到的上下文
- Answer Relevancy: 答案是否回答了问题
- Context Precision: 检索到的上下文是否精准
- Context Recall: 是否检索到了所有相关信息
