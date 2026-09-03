# Day 7 挑战四：数据统计 (★★★★☆)
# 要求: 实现统计分析和可视化。


from collections import Counter, defaultdict
from datetime import datetime, timedelta


def calculate_stats(todos):
    """计算 Todo 列表的综合统计信息。
    
    Returns:
        dict: {
            "total": 总数,
            "completed": 已完成数,
            "pending": 待完成数,
            "completion_rate": 完成率,
            "by_priority": {"高": n, "中": n, "低": n},
            "by_tag": {"tag": n, ...},
            "avg_age_days": 平均存活天数
        }
    """
    # TODO: 实现各项统计计算
    pass


def daily_summary(todos, days=7):
    """生成最近 N 天的每日摘要。
    
    Returns:
        list of dict: 每天的 {date, created, completed, pending}
    """
    # TODO: 按日期分组统计
    pass


def priority_trend(todos, days=30):
    """生成优先级分布趋势。"""
    # TODO: 按日期统计各优先级数量变化
    pass


def generate_text_chart(data, title="", max_width=40):
    """生成字符柱状图。
    
    示例:
        generate_text_chart({"高": 5, "中": 3, "低": 2})
        输出:
          高 | ██████████████████████████ 5
          中 | ███████████████ 3
          低 | ██████████ 2
    
    Args:
        data: {标签: 数值} 字典
        title: 图表标题
        max_width: 最大柱宽
    
    Returns:
        str: 文本图表
    """
    # TODO: 计算最大值，按比例生成 █ 字符
    pass


def generate_progress_bar(completed, total, width=20):
    """生成进度条。"""
    # TODO: 计算填充比例，生成 ████░░░░ 形式
    pass


def format_report(todos):
    """生成完整的文本报告。"""
    # TODO: 组合所有统计信息，生成可读报告
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # 创建测试数据
    class FakeTodo:
        def __init__(self, **kw):
            for k, v in kw.items():
                setattr(self, k, v)
    
    todos = [
        FakeTodo(priority="高", completed=True, tags=["编程"], created_at="2024-01-10"),
        FakeTodo(priority="高", completed=False, tags=["编程"], created_at="2024-01-12"),
        FakeTodo(priority="中", completed=True, tags=["学习"], created_at="2024-01-11"),
        FakeTodo(priority="低", completed=False, tags=["生活"], created_at="2024-01-13"),
    ]
    
    stats = calculate_stats(todos)
    print("统计:", stats)
    
    chart = generate_text_chart({"高": 5, "中": 8, "低": 3}, title="优先级分布")
    print(f"\n{chart}")
    
    bar = generate_progress_bar(3, 7)
    print(f"进度: {bar}")
