# Day 11 - Challenge 1: 工具模块
# 难度: ⭐⭐⭐☆☆
#
# 要求: 创建一个工具模块，包含字符串处理、文件操作、数据验证函数
# 参考 challenge.md

"""
工具模块挑战 — 实现常用的工具函数集合

要求:
- 字符串处理函数 (format_text, truncate, camel_to_snake)
- 文件操作函数 (safe_read, safe_write)
- 数据验证函数 (is_valid_email, is_valid_phone)
- 使用 __all__ 控制导出
"""


def format_text(text: str, width: int = 80, fill_char: str = "*") -> str:
    """格式化文本，居中并用填充字符包裹

    Args:
        text: 要格式化的文本
        width: 总宽度
        fill_char: 填充字符

    Returns:
        格式化后的字符串

    Example:
        >>> format_text("Hello", 20, "=")
        '=======Hello========'
    """
    # TODO: 实现文本居中格式化
    # 1. 计算左右填充长度
    # 2. 拼接 fill_char + text + fill_char
    pass


def truncate(text: str, max_len: int = 100, suffix: str = "...") -> str:
    """截断过长的文本并添加后缀

    Args:
        text: 原始文本
        max_len: 最大长度（包含后缀）
        suffix: 截断后的后缀

    Returns:
        截断后的字符串

    Example:
        >>> truncate("Hello World", 8)
        'Hello...'
    """
    # TODO: 实现文本截断逻辑
    # 如果 len(text) > max_len，截断并加后缀
    pass


def camel_to_snake(name: str) -> str:
    """驼峰命名转下划线命名

    Args:
        name: 驼峰命名字符串

    Returns:
        下划线命名字符串

    Example:
        >>> camel_to_snake("getElementById")
        'get_element_by_id'
    """
    # TODO: 实现驼峰转下划线
    # 提示: 在大写字母前插入下划线，然后转小写
    pass


def safe_read(filepath: str, default: str = "") -> str:
    """安全读取文件内容，出错时返回默认值

    Args:
        filepath: 文件路径
        default: 读取失败时的默认值

    Returns:
        文件内容或默认值
    """
    # TODO: 实现安全文件读取
    # 用 try-except 捕获 FileNotFoundError 和 IOError
    pass


def safe_write(filepath: str, content: str, append: bool = False) -> bool:
    """安全写入文件，出错时返回False

    Args:
        filepath: 文件路径
        content: 要写入的内容
        append: 是否追加模式

    Returns:
        写入是否成功
    """
    # TODO: 实现安全文件写入
    pass


def is_valid_email(email: str) -> bool:
    """验证邮箱格式

    Args:
        email: 邮箱地址

    Returns:
        格式是否有效

    Example:
        >>> is_valid_email("test@example.com")
        True
        >>> is_valid_email("invalid")
        False
    """
    # TODO: 实现邮箱验证（不依赖 re 模块）
    # 检查: 包含 @，@ 前后都有内容，包含 .，域名至少2字符
    pass


def is_valid_phone(phone: str) -> bool:
    """验证手机号格式（中国大陆）

    Args:
        phone: 手机号字符串

    Returns:
        格式是否有效

    Example:
        >>> is_valid_phone("13812345678")
        True
    """
    # TODO: 实现手机号验证
    # 11位数字，1开头
    pass


# 使用 __all__ 控制外部能导入的内容
__all__ = [
    "format_text",
    "truncate",
    "camel_to_snake",
    "safe_read",
    "safe_write",
    "is_valid_email",
    "is_valid_phone",
]


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 工具模块测试 ===")

    # 测试字符串处理
    print(format_text("Hello", 20, "="))
    print(truncate("这是一段很长的文本用来测试截断功能", 10))
    print(camel_to_snake("getElementById"))

    # 测试数据验证
    print(is_valid_email("test@example.com"))
    print(is_valid_phone("138123455678"))

    print("✅ Challenge 01 完成")
