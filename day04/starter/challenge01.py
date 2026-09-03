# Day 4 挑战一：切片大师 (★☆☆☆☆)
# 难度: ★☆☆☆☆
# 要求: 掌握字符串切片的各种用法。


# ===== 任务1: 基础切片 =====
text = "Hello, Python World!"

# TODO: 获取 "Hello"
hello = text[:5]       # 已填写，可直接运行
print(f"Hello: {hello}")

# TODO: 获取 "World"
world = text[-6:-1]    # 已填写
print(f"World: {world}")

# TODO: 获取 "Python"
python = text[7:13]
print(f"Python: {python}")

# TODO: 反转整个字符串
reversed_text = text[::-1]
print(f"反转: {reversed_text}")

# TODO: 每隔一个字符取一个
every_other = text[::2]
print(f"隔一取一: {every_other}")


# ===== 任务2: 实用切片函数 =====

def safe_slice(text, start=0, end=None, step=1):
    """安全切片 —— 自动处理越界，不会抛出异常。
    
    功能说明:
        对字符串进行切片，自动将超出范围的 start/end 调整到合法位置。
    
    示例:
        >>> safe_slice("abc", 0, 100)
        "abc"
        >>> safe_slice("abc", -100, 2)
        "ab"
    
    Args:
        text: 源字符串
        start: 起始位置（可为负数）
        end: 结束位置（可为负数，None 表示到末尾）
        step: 步长
    
    Returns:
        str: 切片结果（保证不抛异常）
    """
    # TODO: 实现安全切片逻辑
    # 提示: 先将负数索引转为正数，再夹紧到 [0, len(text)]
    pass


def extract_between(text, start_marker, end_marker):
    """提取两个标记之间的文本。
    
    功能说明:
        找到 start_marker 和 end_marker 的位置，提取中间的文本。
        支持多个匹配（返回列表）。
    
    示例:
        >>> extract_between("name: Alice, age: Bob", "name: ", ",")
        ["Alice"]
        >>> extract_between("[a] and [b]", "[", "]")
        ["a", "b"]
    
    Args:
        text: 源字符串
        start_marker: 起始标记
        end_marker: 结束标记
    
    Returns:
        list: 所有匹配的中间文本
    """
    # TODO: 实现标记提取逻辑
    pass


def chunk_string(text, chunk_size):
    """将字符串按指定长度分块。
    
    功能说明:
        将字符串每 chunk_size 个字符分为一块。
    
    示例:
        >>> chunk_string("abcdefgh", 3)
        ["abc", "def", "gh"]
    
    Args:
        text: 源字符串
        chunk_size: 每块的字符数
    
    Returns:
        list: 分块后的字符串列表
    """
    # TODO: 使用切片实现分块
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("\n=== safe_slice 测试 ===")
    print(f"safe_slice('Hello', 0, 100): {safe_slice('Hello', 0, 100)}")
    print(f"safe_slice('Hello', -100, 3): {safe_slice('Hello', -100, 3)}")
    
    print("\n=== extract_between 测试 ===")
    html = "<b>粗体</b>普通<b>也是粗体</b>"
    print(f"结果: {extract_between(html, '<b>', '</b>')}")
    
    print("\n=== chunk_string 测试 ===")
    print(f"结果: {chunk_string('abcdefghij', 3)}")
