"""
Challenge 05: RAG 评估方案 (Boss)
整合评估指标、测试管理、自动评估和报告生成。
"""
import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from collections import Counter


@dataclass
class EvalCase:
    """评估用例"""
    query: str
    expected_answer: str
    expected_docs: List[str] = field(default_factory=list)
    category: str = "general"
    difficulty: str = "medium"


@dataclass
class EvalResult:
    """评估结果"""
    case: EvalCase
    retrieved_docs: List[str]
    generated_answer: str
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class EvalReport:
    """评估报告"""
    name: str
    results: List[EvalResult]
    summary: Dict[str, float] = field(default_factory=dict)
    timestamp: str = ""


class RetrievalMetrics:
    """检索质量指标"""

    @staticmethod
    def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
        """Recall@K"""
        # TODO:
        pass

    @staticmethod
    def mrr(retrieved: List[str], relevant: List[str]) -> float:
        """Mean Reciprocal Rank"""
        # TODO:
        pass

    @staticmethod
    def ndcg(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
        """NDCG@K"""
        # TODO:
        pass

    @staticmethod
    def hit_rate(results_list: List[List[str]], relevant_list: List[List[str]]) -> float:
        """Hit Rate"""
        # TODO: 至少一个相关文档在检索结果中的比例
        pass


class GenerationMetrics:
    """生成质量指标"""

    @staticmethod
    def bleu_score(reference: str, candidate: str, max_n: int = 4) -> float:
        """BLEU 分数"""
        # TODO: 简化版 unigram BLEU
        pass

    @staticmethod
    def rouge_l(reference: str, candidate: str) -> float:
        """ROUGE-L 分数"""
        # TODO: 基于 LCS
        pass

    @staticmethod
    def faithfulness(answer: str, context: str) -> float:
        """忠实度：答案中有多少声明能被上下文支持"""
        # TODO: 基于关键词重叠的简化版
        pass

    @staticmethod
    def answer_relevancy(answer: str, query: str) -> float:
        """答案相关性"""
        # TODO: 基于关键词重叠
        pass


class DriftDetector:
    """数据漂移检测器"""

    def __init__(self, baseline_distribution: Dict[str, float] = None):
        self.baseline = baseline_distribution or {}

    def compute_distribution(self, texts: List[str]) -> Dict[str, float]:
        """计算关键词分布"""
        # TODO:
        pass

    def detect_drift(self, current_texts: List[str],
                     threshold: float = 0.1) -> Tuple[bool, float]:
        """检测漂移（KL散度）"""
        # TODO: 计算当前分布与基线的 KL 散度
        pass


class RAGEvalSuite:
    """RAG 评估套件"""

    def __init__(self, name: str = "default"):
        self.name = name
        self.test_cases: List[EvalCase] = []
        self.results: List[EvalResult] = []
        self.retrieval_metrics = RetrievalMetrics()
        self.generation_metrics = GenerationMetrics()
        self.drift_detector = DriftDetector()

    def add_test_cases(self, cases: List[EvalCase]):
        """添加测试用例"""
        # TODO:
        pass

    def evaluate(self, rag_func: Callable) -> EvalReport:
        """
        运行评估。
        rag_func: 接收 query 返回 {"answer": str, "sources": List[str]}
        """
        # TODO: 对每个测试用例调用 rag_func，计算指标，生成报告
        pass

    def compare(self, rag_func_a: Callable, rag_func_b: Callable,
                runs: int = 5) -> Dict:
        """
        A/B 对比评估。
        返回: {"winner": str, "p_value": float, "scores": Dict}
        """
        # TODO: 多次运行，统计显著性检验
        pass

    def generate_report(self, results: List[EvalResult] = None) -> EvalReport:
        """生成评估报告"""
        # TODO: 汇总所有指标的均值、标准差、按类别的分数
        pass

    def render_ascii_report(self, report: EvalReport) -> str:
        """渲染 ASCII 可视化报告"""
        # TODO: 生成柱状图和表格
        pass

    def check_drift(self, new_texts: List[str]) -> Tuple[bool, str]:
        """检查数据漂移"""
        # TODO:
        pass

    # ---- pytest 集成 ----
    def pytest_fixture(self, rag_func: Callable):
        """返回 pytest fixture 可用的评估函数"""
        # TODO:
        pass


# 测试
if __name__ == "__main__":
    suite = RAGEvalSuite("RAG 测试套件")

    # 添加测试用例
    suite.add_test_cases([
        EvalCase("Python 是什么？", "Python 是编程语言", ["doc1"], "基础"),
        EvalCase("列表推导式语法？", "[x for x in range(10)]", ["doc2"], "语法"),
    ])

    # 模拟 RAG 函数
    def mock_rag(query: str) -> Dict:
        return {"answer": "Python 是一种编程语言", "sources": ["doc1"]}

    report = suite.evaluate(mock_rag)
    print(f"评估完成: {len(report.results)} 个用例")
    print(f"汇总: {report.summary}")
    print(suite.render_ascii_report(report))
