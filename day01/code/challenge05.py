# Boss Challenge: 多格式报告生成器
# Day 1 - 难度: ★★★★★
#
# 只用 Day 1 学到的函数参数知识。
# 参考 README.md 了解具体要求。

def generate_report(title, headers, rows, format="text", separator=",", 
                    show_total=False, sort_by=None, max_width=None):
    """生成格式化报告"""
    # TODO: 实现报告生成逻辑
    pass


def print_report(*columns, **options):
    """打印报告的便捷接口"""
    # TODO
    pass


def compare_reports(*reports, show_diff=False):
    """对比多份报告"""
    # TODO
    pass


if __name__ == "__main__":
    headers = ["Name", "Age", "Score"]
    rows = [
        ["Alice", 20, 85],
        ["Bob", 22, 92],
        ["Charlie", 20, 78],
    ]
    print("Boss Challenge: 多格式报告生成器")
    print("请实现所有 TODO 方法")
