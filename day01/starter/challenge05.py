# Day 1 挑战五 (Boss)：多格式报告生成器 (★★★★★)
# 难度: ★★★★★
# 要求: 用函数参数构建支持多种输出格式的报告生成器。


def generate_report(title, data, *, format="text", include_summary=True, 
                    precision=2, sort_by=None, descending=False):
    """生成支持多种输出格式的数据报告。
    
    功能说明:
        接收报告标题和数据，根据 format 参数生成不同格式的报告。
        支持 text（纯文本）、markdown、csv 三种格式。
    
    示例:
        >>> data = [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}]
        >>> print(generate_report("成绩报告", data, format="text"))
        >>> print(generate_report("成绩报告", data, format="markdown"))
        >>> print(generate_report("成绩报告", data, format="csv"))
    
    Args:
        title: 报告标题（字符串）
        data: 数据列表，每个元素是一个字典
        format: 输出格式，可选 "text"/"markdown"/"csv"，默认 "text"
        include_summary: 是否包含汇总统计，默认 True
        precision: 数值精度（小数位数），默认 2
        sort_by: 排序字段名（可选），默认 None 不排序
        descending: 是否降序排列，默认 False
    
    Returns:
        str: 格式化后的报告字符串
    
    Raises:
        ValueError: 当 format 不是合法值时
        KeyError: 当 sort_by 指定的字段不存在于数据中时
    """
    # TODO: 步骤1 - 验证参数（format 合法性、data 非空）
    # TODO: 步骤2 - 如果指定了 sort_by，对 data 排序
    # TODO: 步骤3 - 根据 format 调用对应的格式化函数
    # TODO: 步骤4 - 如果 include_summary，附加汇总信息
    pass


def _format_text(title, data, precision, summary=None):
    """将数据格式化为纯文本报告。
    
    Args:
        title: 报告标题
        data: 数据列表
        precision: 数值精度
        summary: 可选的汇总信息字典
    
    Returns:
        str: 纯文本格式的报告
    """
    # TODO: 生成带边框的纯文本表格
    # TODO: 自动计算列宽
    pass


def _format_markdown(title, data, precision, summary=None):
    """将数据格式化为 Markdown 表格报告。
    
    Args:
        title: 报告标题
        data: 数据列表
        precision: 数值精度
        summary: 可选的汇总信息字典
    
    Returns:
        str: Markdown 格式的报告
    """
    # TODO: 生成 Markdown 表格（带表头和分隔线）
    pass


def _format_csv(title, data, precision, summary=None):
    """将数据格式化为 CSV 格式报告。
    
    Args:
        title: 报告标题
        data: 数据列表
        precision: 数值精度
        summary: 可选的汇总信息字典
    
    Returns:
        str: CSV 格式的报告（带标题行注释）
    """
    # TODO: 生成 CSV 格式字符串（包含标题注释行）
    pass


def calculate_summary(data):
    """计算数据的汇总统计信息。
    
    功能说明:
        遍历数据中的所有数值字段，计算每个字段的
        count、sum、avg、min、max。
    
    Args:
        data: 字典列表
    
    Returns:
        dict: 汇总统计信息
        {
            "字段名": {
                "count": 数量, "sum": 总和,
                "avg": 平均值, "min": 最小值, "max": 最大值
            }
        }
    """
    # TODO: 步骤1 - 识别所有数值类型的字段
    # TODO: 步骤2 - 对每个数值字段计算统计指标
    # TODO: 步骤3 - 返回汇总字典
    pass


# ===== 测试 =====
if __name__ == "__main__":
    data = [
        {"name": "Alice", "score": 95, "grade": "A"},
        {"name": "Bob", "score": 87, "grade": "B"},
        {"name": "Charlie", "score": 92, "grade": "A"},
        {"name": "Diana", "score": 78, "grade": "C"},
    ]
    
    print("=" * 50)
    print("【纯文本格式】")
    print(generate_report("成绩报告", data, format="text", sort_by="score", descending=True))
    
    print("\n" + "=" * 50)
    print("【Markdown 格式】")
    print(generate_report("成绩报告", data, format="markdown"))
    
    print("\n" + "=" * 50)
    print("【CSV 格式】")
    print(generate_report("成绩报告", data, format="csv"))
