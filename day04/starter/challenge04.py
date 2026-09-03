# Day 4 挑战四：正则提取器 (★★★★☆)
# 难度: ★★★★☆
# 要求: 使用正则表达式进行各种文本提取和匹配。


import re
from datetime import datetime


def extract_emails(text):
    """从文本中提取所有邮箱地址。
    
    示例:
        >>> extract_emails("联系 alice@example.com 或 bob@test.org")
        ["alice@example.com", "bob@test.org"]
    
    Args:
        text: 源文本
    
    Returns:
        list: 所有匹配的邮箱地址
    """
    # TODO: 编写邮箱正则并使用 re.findall
    pass


def extract_urls(text):
    """从文本中提取所有 URL（HTTP/HTTPS）。
    
    示例:
        >>> extract_urls("访问 https://example.com 和 http://test.org/page")
        ["https://example.com", "http://test.org/page"]
    
    Args:
        text: 源文本
    
    Returns:
        list: 所有匹配的 URL
    """
    # TODO: 编写 URL 正则
    pass


def extract_chinese(text):
    """提取文本中的所有中文字符。
    
    示例:
        >>> extract_chinese("Hello 你好 World 世界")
        ["你好", "世界"]
    
    Args:
        text: 源文本
    
    Returns:
        list: 所有连续的中文字符串
    """
    # TODO: 使用 Unicode 范围匹配中文
    pass


def extract_numbers(text):
    """提取文本中的所有数字（包括负数、小数）。
    
    示例:
        >>> extract_numbers("温度 -3.5°C，湿度 68%")
        ["-3.5", "68"]
    
    Args:
        text: 源文本
    
    Returns:
        list: 所有匹配的数字字符串
    """
    # TODO: 编写数字正则（支持负号和小数点）
    pass


def extract_dates(text):
    """提取文本中的日期（支持多种格式）。
    
    支持格式:
        - YYYY-MM-DD
        - YYYY/MM/DD
        - YYYY年MM月DD日
    
    示例:
        >>> extract_dates("成立于 2024-01-15，更新于 2024年3月20日")
        ["2024-01-15", "2024年3月20日"]
    
    Args:
        text: 源文本
    
    Returns:
        list: 所有匹配的日期字符串
    """
    # TODO: 编写日期正则（支持多种分隔符）
    pass


def extract_structured(text, pattern, groups=None):
    """通用结构化提取器 —— 使用命名捕获组提取数据。
    
    功能说明:
        根据给定的正则模式提取数据，可选指定组名映射。
    
    示例:
        >>> text = "张三,年龄25,北京"
        >>> extract_structured(text, r'(?P<name>\w+),年龄(?P<age>\d+),(?P<city>\w+)')
        [{"name": "张三", "age": "25", "city": "北京"}]
    
    Args:
        text: 源文本
        pattern: 正则模式（支持命名捕获组）
        groups: 可选的组名列表
    
    Returns:
        list of dict: 每个匹配结果的字典
    """
    # TODO: 使用 re.finditer + groupdict 提取结构化数据
    pass


def replace_pattern(text, pattern, replacement):
    """按正则模式替换文本（支持回调函数）。
    
    功能说明:
        replacement 可以是字符串（支持反向引用 \1, \g<name>），
        也可以是函数（接收 Match 对象）。
    
    Args:
        text: 源文本
        pattern: 正则模式
        replacement: 替换内容或回调函数
    
    Returns:
        str: 替换后的文本
    """
    # TODO: 使用 re.sub 实现模式替换
    pass


# ===== 测试 =====
if __name__ == "__main__":
    sample = """
    联系方式：
    - 邮箱: alice@example.com, bob@test.org
    - 网站: https://example.com, http://blog.test.org
    - 日期: 2024-01-15, 2024年3月20日
    - 温度: -3.5°C ~ 28.3°C
    - 中文内容：这是一段测试文本
    """
    
    print("=== 邮箱 ===")
    print(extract_emails(sample))
    
    print("\n=== URL ===")
    print(extract_urls(sample))
    
    print("\n=== 中文 ===")
    print(extract_chinese(sample))
    
    print("\n=== 数字 ===")
    print(extract_numbers(sample))
    
    print("\n=== 日期 ===")
    print(extract_dates(sample))
