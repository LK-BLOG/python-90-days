# Day 4 挑战二：文本清洗器 (★★☆☆☆)
# 难度: ★★☆☆☆
# 要求: 实现各种文本清洗和规范化操作。


import re


def clean_text(text):
    """基础文本清洗 —— 去除多余空白、统一空格。
    
    功能说明:
        - 去除首尾空白
        - 将多个连续空格替换为单个空格
        - 将制表符替换为空格
        - 移除空行
    
    示例:
        >>> clean_text("  Hello   World  \\n\\n  Python  ")
        "Hello World Python"
    
    Args:
        text: 原始文本
    
    Returns:
        str: 清洗后的文本
    """
    # TODO: 实现文本清洗逻辑
    pass


def normalize_whitespace(text, replacement=" "):
    """统一空白字符 —— 将所有空白字符替换为指定字符。
    
    Args:
        text: 原始文本
        replacement: 替换字符，默认单个空格
    
    Returns:
        str: 规范化后的文本
    """
    # TODO: 使用 re.sub 将 \s+ 替换
    pass


def remove_punctuation(text):
    """移除标点符号。
    
    功能说明:
        移除所有 ASCII 标点符号和中文标点符号，保留字母、数字、中文、空格。
    
    Args:
        text: 原始文本
    
    Returns:
        str: 移除标点后的文本
    """
    # TODO: 使用正则表达式匹配并移除标点
    pass


def to_snake_case(name):
    """将各种命名格式转为 snake_case。
    
    功能说明:
        支持 camelCase、PascalCase、kebab-case、空格分隔 等格式。
    
    示例:
        >>> to_snake_case("CamelCase")
        "camel_case"
        >>> to_snake_case("my-variable-name")
        "my_variable_name"
        >>> to_snake_case("Hello World")
        "hello_world"
    
    Args:
        name: 原始名称
    
    Returns:
        str: snake_case 格式的名称
    """
    # TODO: 在大写字母前插入下划线
    # TODO: 将连字符、空格替换为下划线
    # TODO: 转小写
    pass


def mask_sensitive(text, pattern=r'\b\d{4,}\b', mask_char='*'):
    """敏感信息脱敏 —— 按正则匹配替换为掩码。
    
    功能说明:
        找到匹配 pattern 的子串，将其首尾各保留1个字符，中间用 mask_char 替换。
    
    示例:
        >>> mask_sensitive("卡号: 6222021234567890")
        "卡号: 6222****7890"
    
    Args:
        text: 原始文本
        pattern: 匹配模式（默认匹配4位以上连续数字）
        mask_char: 掩码字符
    
    Returns:
        str: 脱敏后的文本
    """
    # TODO: 使用 re.sub 和回调函数实现脱敏
    pass


# ===== 测试 =====
if __name__ == "__main__":
    raw = "  Hello   World!  \\n  Python is  Great.  "
    print(f"原文: '{raw}'")
    print(f"清洗: '{clean_text(raw)}'")
    
    print(f"\nsnake_case:")
    print(f"  CamelCase -> {to_snake_case('CamelCase')}")
    print(f"  my-variable -> {to_snake_case('my-variable-name')}")
    print(f"  Hello World -> {to_snake_case('Hello World')}")
    
    print(f"\n脱敏:")
    print(f"  卡号: {mask_sensitive('卡号: 6222021234567890')}")
    print(f"  手机: {mask_sensitive('手机: 13812345678', r'1[3-9]\\d{9}')}")
