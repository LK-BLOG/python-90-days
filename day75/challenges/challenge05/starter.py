"""
Challenge 05: 完整文档助手 (Boss)
整合查询、对话管理、引用溯源和 API 封装。
"""
import json
import time
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Generator
from pathlib import Path
from datetime import datetime


@dataclass
class Citation:
    """引用"""
    doc_id: str
    doc_name: str
    chunk_text: str
    page: int = 0
    confidence: str = "medium"  # high/medium/low


@dataclass
class DocAnswer:
    """文档问答结果"""
    answer: str
    citations: List[Citation]
    confidence: float
    conversation_id: str = ""


@dataclass
class Conversation:
    """对话"""
    id: str
    messages: List[Dict] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class Feedback:
    """用户反馈"""
    conversation_id: str
    message_index: int
    rating: int  # 1 or -1
    comment: str = ""


class QueryRewriter:
    """查询改写器"""

    def rewrite(self, query: str, history: List[Dict] = None) -> str:
        """改写查询（消解指代、扩展关键词）"""
        # TODO: 基于对话历史消解指代
        # "它的作者是谁" → "《Python》的作者是谁"
        pass

    def generate_variants(self, query: str, n: int = 3) -> List[str]:
        """生成查询变体"""
        # TODO: 生成 n 个不同角度的查询
        pass


class Reranker:
    """重排序器"""

    def rerank(self, query: str, results: List[Dict],
               top_k: int = 5) -> List[Dict]:
        """对检索结果重排序"""
        # TODO: 基于查询与结果的关键词匹配度重排
        pass


class ConversationManager:
    """对话管理器"""

    def __init__(self, max_history: int = 20):
        self.conversations: Dict[str, Conversation] = {}
        self.max_history = max_history

    def create(self) -> str:
        """创建新对话"""
        # TODO: 生成 conversation_id
        pass

    def add_message(self, conv_id: str, role: str, content: str):
        """添加消息"""
        # TODO:
        pass

    def get_messages(self, conv_id: str, last_n: int = None) -> List[Dict]:
        """获取消息"""
        # TODO:
        pass

    def compress_history(self, conv_id: str) -> str:
        """压缩历史（摘要）"""
        # TODO: 将长对话压缩为摘要
        pass

    def save(self, filepath: str):
        """持久化到文件"""
        # TODO:
        pass

    def load(self, filepath: str):
        """从文件恢复"""
        # TODO:
        pass


class FeedbackCollector:
    """反馈收集器"""

    def __init__(self):
        self.feedbacks: List[Feedback] = []

    def submit(self, conversation_id: str, message_index: int,
               rating: int, comment: str = ""):
        """提交反馈"""
        # TODO:
        pass

    def get_summary(self, conversation_id: str = None) -> Dict:
        """获取反馈汇总"""
        # TODO: 正面/负面比例、常见评论
        pass


class DocAssistant:
    """文档问答助手"""

    def __init__(self, max_context_tokens: int = 3000):
        self.rewriter = QueryRewriter()
        self.reranker = Reranker()
        self.conv_manager = ConversationManager()
        self.feedback_collector = FeedbackCollector()
        self.documents: Dict[str, Dict] = {}
        self.index: List[Dict] = []  # 简易向量索引
        self.max_context_tokens = max_context_tokens

    # ---- 文档管理 ----
    def upload_document(self, doc_id: str, content: str,
                        metadata: Dict = None) -> int:
        """上传文档，返回 chunk 数"""
        # TODO: 分块 + 索引
        pass

    # ---- 对话 ----
    def chat(self, message: str, conversation_id: str = None) -> DocAnswer:
        """
        多轮对话。
        流程: 查询改写 → 检索 → 重排序 → 生成答案 → 引用溯源
        """
        # TODO:
        pass

    def stream_chat(self, message: str,
                    conversation_id: str = None) -> Generator[str, None, None]:
        """流式对话"""
        # TODO: 逐 token 输出
        yield ""

    # ---- 检索 ----
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """纯检索（不经过 LLM）"""
        # TODO:
        pass

    def _retrieve(self, query: str, top_k: int = 10) -> List[Dict]:
        """向量检索"""
        # TODO: 简易余弦相似度
        pass

    # ---- 引用 ----
    def _build_citations(self, results: List[Dict]) -> List[Citation]:
        """构建引用列表"""
        # TODO:
        pass

    # ---- 反馈 ----
    def submit_feedback(self, conversation_id: str, message_index: int,
                        rating: int, comment: str = ""):
        """提交反馈"""
        # TODO:
        pass

    # ---- 对话管理 ----
    def get_conversations(self) -> List[Dict]:
        """获取对话列表"""
        # TODO:
        pass

    def delete_conversation(self, conv_id: str):
        """删除对话"""
        # TODO:
        pass

    # ---- API 定义 ----
    def api_endpoints(self) -> List[Dict]:
        """返回 API 端点定义"""
        return [
            {"method": "POST", "path": "/chat", "description": "多轮对话"},
            {"method": "POST", "path": "/upload", "description": "上传文档"},
            {"method": "GET", "path": "/search", "description": "纯检索"},
            {"method": "GET", "path": "/conversations", "description": "对话列表"},
            {"method": "DELETE", "path": "/conversations/{id}", "description": "删除对话"},
            {"method": "WebSocket", "path": "/ws/chat", "description": "实时对话"},
        ]


# 测试
if __name__ == "__main__":
    assistant = DocAssistant()
    assistant.upload_document("doc1", "Python 是一种解释型高级编程语言，由 Guido van Rossum 于 1991 年创建。")
    assistant.upload_document("doc2", "机器学习是人工智能的核心分支，深度学习是机器学习的子集。")

    conv_id = assistant.conv_manager.create()
    result = assistant.chat("Python 是什么？", conv_id)
    print(f"答案: {result.answer}")
    print(f"引用: {[(c.doc_name, c.confidence) for c in result.citations]}")

    # 流式输出
    print("流式: ", end="")
    for token in assistant.stream_chat("机器学习是什么？", conv_id):
        print(token, end="", flush=True)
    print()

    # API 定义
    for ep in assistant.api_endpoints():
        print(f"  {ep['method']} {ep['path']} - {ep['description']}")
