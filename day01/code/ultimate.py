# Boss Challenge: 多格式报告生成器
# Day 1 - 难度: ★★★★★
#
# 只用 Day 1 学到的函数参数知识，不依赖任何其他概念。
# 参考 README.md 了解具体要求。

def generate_report(title, headers, rows, format="text", separator=",", 
                    show_total=False, sort_by=None, max_width=None):
    """生成格式化报告
    
    Args:
        title: 报告标题 (str)
        headers: 列名列表 (list[str])
        rows: 数据行 (list[list])
        format: 输出格式 "text"/"csv"/"markdown"/"html"
        separator: CSV分隔符 (str)
        show_total: 是否显示数字列统计 (bool)
        sort_by: 按第几列排序 (int or None)
        max_width: text格式最大列宽 (int or None)
    
    Returns:
        格式化的报告字符串 (str)
    """
    # TODO: 实现报告生成逻辑
    # 提示：根据 format 参数选择不同的输出格式
    # 提示：先处理排序（如果有的话）
    # 提示：最后处理统计行（如果需要的话）
    pass


def _format_text(title, headers, rows, max_width=None):
    """纯文本表格格式"""
    # TODO: 实现文本对齐表格
    # 提示：计算每列的最大宽度，然后用 | 和 - 拼接
    pass


def _format_csv(headers, rows, separator=","):
    """CSV格式"""
    # TODO: 实现CSV输出
    pass


def _format_markdown(headers, rows):
    """Markdown表格格式"""
    # TODO: 实现Markdown表格
    pass


def _format_html(title, headers, rows):
    """HTML表格格式"""
    # TODO: 实现HTML表格
    pass


def print_report(*columns, **options):
    """打印报告的便捷接口
    
    *columns: 任意数量的列数据
    **options: 所有格式选项（format/separator/sort_by等）
    """
    # TODO: 实现便捷接口
    pass


def compare_reports(*reports, show_diff=False):
    """对比多份报告
    
    *reports: 任意数量的报告字符串
    show_diff: 是否高亮差异
    """
    # TODO: 实现报告对比
    pass


if __name__ == "__main__":
    headers = ["Name", "Age", "Score"]
    rows = [
        ["Alice", 20, 85],
        ["Bob", 22, 92],
        ["Charlie", 20, 78],
        ["Diana", 21, 95],
    ]
    
    print("Boss Challenge: 多格式报告生成器")
    print("=" * 40)
    print("请实现所有 TODO 方法")
    print("只用 Day 1 学到的函数参数知识！")
