# Day 80 - Example 1: Token计数器
# 展示字符级近似和tiktoken精确计数的对比

import sys
from typing import Optional

# ===== 方式1: 字符级近似计数 =====
def approx_tokens(text: str) -> int:
    """
    近似计算Token数
    - ASCII字符: 约4个字符 = 1 token
    - 非ASCII(中文等): 约1.5个字符 = 1 token
    """
    ascii_count = sum(1 for c in text if ord(c) < 128)
    non_ascii_count = len(text) - ascii_count
    return max(1, (ascii_count / 4 + non_ascii_count / 1.5).__ceil__())

# ===== 方式2: tiktoken精确计数 =====
def exact_tokens(text: str, model: str = "gpt-4") -> Optional[int]:
    """
    使用tiktoken精确计算Token数
    需要: pip install tiktoken
    """
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except ImportError:
        print("提示: pip install tiktoken 以使用精确计数")
        return None
    except KeyError:
        print(f"未知模型: {model}, 使用cl100k_base")
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


def compare_counting(text: str):
    """对比近似和精确计数"""
    approx = approx_tokens(text)
    exact = exact_tokens(text)

    print(f"文本: {text[:50]}...")
    print(f"  字符数: {len(text)}")
    print(f"  近似Token: {approx}")
    if exact is not None:
        diff = abs(approx - exact)
        error_rate = diff / exact * 100
        print(f"  精确Token: {exact}")
        print(f"  误差: {diff} ({error_rate:.1f}%)")
    print()


if __name__ == "__main__":
    test_cases = [
        "Hello, world!",
        "这是一个中文测试文本。",
        "Mixed English and 中文混合文本 test.",
        "Python is a programming language. Python是一种编程语言。两者是同一种东西。",
        "def hello():\n    print('Hello, World!')\n\nfor i in range(10):\n    hello()",
    ]

    print("=" * 60)
    print("Token计数器对比测试")
    print("=" * 60)

    for text in test_cases:
        compare_counting(text)

    # 演示预算计算
    print("=" * 60)
    print("预算计算演示")
    print("=" * 60)
    budget = 128000
    system_prompt = "你是一个数据分析助手，擅长Python和SQL。请用中文回答。"
    print(f"总预算: {budget} tokens")
    print(f"System Prompt近似: {approx_tokens(system_prompt)} tokens")

    # 模拟多轮对话
    sample_conversation = [
        {"role": "user", "content": "帮我分析这个数据集的趋势"},
        {"role": "assistant", "content": "好的，我来帮你分析。首先让我看看数据的基本统计信息..."},
        {"role": "user", "content": "按月份分组看看"},
        {"role": "assistant", "content": "好的，按月份分组后，我发现了以下趋势：1月到3月呈上升趋势..."},
    ] * 10  # 模拟50轮对话

    total = sum(approx_tokens(m["content"]) for m in sample_conversation)
    print(f"50轮对话近似: {total} tokens")
    print(f"剩余给System: {budget - total} tokens")
