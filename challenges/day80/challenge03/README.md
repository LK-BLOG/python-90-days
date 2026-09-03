# Day 80 Challenge 3: 上下文压缩器 ⭐⭐⭐
# 实现多种上下文压缩策略

"""
实现三种压缩策略：
1. SummaryCompression: 摘要压缩（模拟LLM摘要）
2. ExtractiveCompression: 关键信息提取
3. SmartCompression: 智能组合策略

输入: 消息列表 + 目标Token数
输出: 压缩后的消息列表，确保不超过目标Token数
"""

from typing import List, Dict, Callable

class CompressionStrategy:
    def compress(self, messages: List[Dict], target_tokens: int, count_fn: Callable) -> List[Dict]:
        pass


class SummaryCompression(CompressionStrategy):
    def __init__(self):
        pass
    def compress(self, messages, target_tokens, count_fn):
        # TODO: 模拟LLM摘要（可以用简单的截断+标注代替）
        pass


class ExtractiveCompression(CompressionStrategy):
    def compress(self, messages, target_tokens, count_fn):
        # TODO: 提取关键消息（包含关键词的、用户消息等）
        pass


class SmartCompression(CompressionStrategy):
    def __init__(self, summary_threshold: float = 0.7):
        pass
    def compress(self, messages, target_tokens, count_fn):
        # TODO: 先尝试提取，不够再摘要
        pass


if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "我想学习Python"},
        {"role": "assistant", "content": "好的！Python是一门很好的语言。"},
        {"role": "user", "content": "重要：我需要在本周五前完成项目"},
        {"role": "assistant", "content": "了解，项目截止日期是本周五。"},
        {"role": "user", "content": "给我推荐一些学习资源"},
    ]
    # 测试压缩
    pass
