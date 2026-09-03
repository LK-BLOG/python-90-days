# Day 11 - Challenge 5: 模块化重构
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 将一个大文件按职责拆分为多个模块，重构已有代码
# 参考 challenge.md

"""
模块化重构挑战 — 学会识别代码职责并拆分模块

任务:
- 识别一个 "大泥球" 函数的职责
- 按单一职责原则拆分为多个函数
- 添加模块级别的常量和配置
- 用 __all__ 控制对外接口
"""

from dataclasses import dataclass


# ===== 重构前: 一个大函数干所有事 =====
def process_data_old(data: list) -> dict:
    """[这是重构前的代码 — 不要修改它，作为参考]

    这个函数干了太多事：清洗、转换、统计、格式化
    违反了单一职责原则
    """
    cleaned = []
    for item in data:
        if isinstance(item, str) and item.strip():
            cleaned.append(item.strip().lower())
        elif isinstance(item, (int, float)):
            cleaned.append(item)

    numbers = [x for x in cleaned if isinstance(x, (int, float))]
    strings = [x for x in cleaned if isinstance(x, str)]

    stats = {
        "count": len(cleaned),
        "num_count": len(numbers),
        "str_count": len(strings),
        "num_sum": sum(numbers),
        "num_avg": sum(numbers) / len(numbers) if numbers else 0,
    }

    result = {"cleaned": cleaned, "stats": stats}
    return result


# ===== 重构后: 按职责拆分 =====

# --- 模块常量 ---
MIN_STRING_LENGTH = 1  # 最小字符串长度
TRIM_WHITESPACE = True  # 是否去除首尾空白
CONVERT_TO_LOWER = True  # 是否转小写


@dataclass
class DataStats:
    """数据统计结果

    Attributes:
        count: 总条数
        num_count: 数字条数
        str_count: 字符串条数
        num_sum: 数字总和
        num_avg: 数字平均值
    """
    count: int = 0
    num_count: int = 0
    str_count: int = 0
    num_sum: float = 0
    num_avg: float = 0


def clean_item(item) -> str | int | float | None:
    """清洗单个数据项

    Args:
        item: 原始数据项

    Returns:
        清洗后的值，无效数据返回 None
    """
    # TODO: 实现单个数据清洗
    # 1. 字符串: 去空白 + 可选转小写
    # 2. 数字: 直接返回
    # 3. 其他: 返回 None
    pass


def clean_data(data: list) -> list:
    """清洗整个数据列表

    Args:
        data: 原始数据列表

    Returns:
        清洗后的列表（过滤掉 None）
    """
    # TODO: 用 clean_item 逐个清洗，过滤 None
    pass


def compute_stats(data: list) -> DataStats:
    """计算数据统计

    Args:
        data: 已清洗的数据列表

    Returns:
        DataStats 实例
    """
    # TODO: 分离数字和字符串，计算统计信息
    pass


def format_report(stats: DataStats) -> str:
    """格式化统计报告

    Args:
        stats: DataStats 实例

    Returns:
        格式化的多行字符串报告
    """
    # TODO: 返回美观的报告字符串
    pass


def process_data(data: list) -> dict:
    """重构后的主函数 — 协调各模块

    Args:
        data: 原始数据列表

    Returns:
        {"cleaned": [...], "stats": DataStats, "report": "..."}
    """
    # TODO: 调用各子函数，返回整合结果
    pass


# __all__ 控制导出
__all__ = [
    "DataStats",
    "clean_item",
    "clean_data",
    "compute_stats",
    "format_report",
    "process_data",
]


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 模块化重构测试 ===")

    raw = [" Hello ", 42, "", "world", 3.14, None, "  ", 100, True]
    result = process_data(raw)

    print(f"清洗后: {result['cleaned']}")
    print(f"统计: {result['stats']}")
    print(f"报告:\n{result.get('report', '(未实现)')}")

    # 验证重构前后结果一致
    old = process_data_old(raw)
    assert result["stats"].count == old["stats"]["count"], "数量不一致!"
    print("重构一致性: ✅")

    print("✅ Challenge 05 完成")
