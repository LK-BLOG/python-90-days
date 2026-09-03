"""
Challenge 05: QA 系统 (Boss)
整合分块、向量存储、嵌入和 RAG 管道为完整 QA 系统。
"""
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class Document:
    """文档"""
    doc_id: str
    content: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class Chunk:
    """文档块"""
    chunk_id: str
    doc_id: str
    text: str
    start_idx: int
    end_idx: int
    metadata: Dict = field(default_factory=dict)


@dataclass
class SearchResult:
    """检索结果"""
    chunk: Chunk
    score: float
    embedding: np.ndarray = None


@dataclass
class QAResult:
    """QA 结果"""
    answer: str
    sources: List[Dict]
    confidence: float


class DocumentChunker:
    """文档分块器"""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, doc: Document) -> List[Chunk]:
        """将文档分块"""
        # TODO: 按段落优先 + 滑动窗口分块
        pass


class SimpleVectorStore:
    """简易向量存储"""

    def __init__(self):
        self.chunks: List[Chunk] = []
        self.embeddings: List[np.ndarray] = []

    def add(self, chunk: Chunk, embedding: np.ndarray):
        """添加向量"""
        # TODO:
        pass

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """余弦相似度检索"""
        # TODO:
        pass

    def delete(self, doc_id: str):
        """删除指定文档的所有块"""
        # TODO:
        pass


class EmbeddingService:
    """嵌入服务"""

    def embed(self, texts: List[str]) -> List[np.ndarray]:
        """生成嵌入向量（模拟）"""
        # TODO: 返回伪随机向量用于测试
        pass

    def embed_query(self, query: str) -> np.ndarray:
        """生成查询嵌入"""
        # TODO:
        pass


class QASystem:
    """QA 问答系统"""

    def __init__(self, chunk_size: int = 500, overlap: int = 50, top_k: int = 3):
        self.chunker = DocumentChunker(chunk_size, overlap)
        self.store = SimpleVectorStore()
        self.embedder = EmbeddingService()
        self.top_k = top_k
        self.conversation_history: List[Dict] = []

    def ingest(self, documents: List[Document]) -> int:
        """导入文档，返回 chunk 数量"""
        # TODO: 分块 → 嵌入 → 存储
        pass

    def query(self, question: str) -> QAResult:
        """
        查询并返回答案。
        流程: 查询嵌入 → 向量检索 → 构建 Prompt → 生成答案
        """
        # TODO:
        pass

    def _build_prompt(self, question: str, contexts: List[SearchResult]) -> str:
        """构建包含上下文的 Prompt"""
        # TODO:
        pass

    def _generate_answer(self, prompt: str) -> Tuple[str, float]:
        """调用 LLM 生成答案（模拟）"""
        # TODO: 返回模拟答案和置信度
        pass

    def _extract_sources(self, results: List[SearchResult]) -> List[Dict]:
        """提取引用来源"""
        # TODO:
        pass

    def evaluate_answer(self, question: str, answer: str,
                        contexts: List[str]) -> Dict:
        """
        评估答案质量。
        返回: {"relevancy": float, "faithfulness": float}
        """
        # TODO: 基于关键词重叠的简单评估
        pass


# 测试
if __name__ == "__main__":
    qa = QASystem(chunk_size=200, overlap=20)
    docs = [
        Document("doc1", "Python 是一种解释型编程语言。Python 支持多种编程范式。", {"title": "Python 简介"}),
        Document("doc2", "机器学习是人工智能的一个分支。深度学习使用神经网络。", {"title": "机器学习入门"}),
    ]
    count = qa.ingest(docs)
    print(f"导入完成: {count} 个 chunks")
    result = qa.query("Python 是什么？")
    print(f"答案: {result.answer}")
    print(f"来源: {result.sources}")
