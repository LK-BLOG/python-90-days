# Day 1 挑战一：参数变形器 (★☆☆☆☆)
# 难度: ★☆☆☆☆
# 要求: 编写一个函数，接收任意位置参数和关键字参数，返回格式化的信息字符串。

def format_info(*args, **kwargs):
    """接收任意位置参数和关键字参数，返回格式化的信息字符串。
    
    功能说明:
        将传入的位置参数作为"人员"列表，关键字参数作为"附加信息"，
        拼接成一个格式化的信息字符串。
    
    示例:
        >>> format_info("Alice", "Bob", city="北京", age=25)
        "人员: Alice, Bob | 附加信息: city=北京, age=25"
        >>> format_info("张三")
        "人员: 张三 | 附加信息: 无"
    
    Args:
        *args: 任意数量的位置参数（期望为字符串，非字符串自动转为str）
        **kwargs: 任意关键字参数，用于附加额外信息
    
    Returns:
        str: 格式化后的信息字符串，格式为 "人员: xxx | 附加信息: xxx"
    
    Raises:
        无异常，所有输入都会被转为字符串处理
    """
    # TODO: 步骤1 - 将 args 中的元素用 ", " 连接成人员列表字符串
    # TODO: 步骤2 - 将 kwargs 中的键值对格式化为 "key=value" 形式并用 ", " 连接
    # TODO: 步骤3 - 如果没有附加信息，显示 "无"
    # TODO: 步骤4 - 拼接最终字符串并返回
    pass


def format_table(*headers, rows):
    """根据表头和数据行生成文本表格。
    
    功能说明:
        接收任意数量的表头字符串和一个 rows 列表（每个元素是一行数据的元组/列表），
        生成一个对齐的文本表格字符串。
    
    示例:
        >>> print(format_table("姓名", "年龄", rows=[("Alice", 25), ("Bob", 30)]))
        姓名   年龄
        ----   ----
        Alice  25
        Bob    30
    
    Args:
        *headers: 表头字符串（任意数量）
        rows: 关键字参数，值为可迭代的行数据
    
    Returns:
        str: 格式化后的文本表格
    """
    # TODO: 步骤1 - 计算每列的最大宽度
    # TODO: 步骤2 - 生成表头行和分隔线
    # TODO: 步骤3 - 遍历 rows 生成数据行
    # TODO: 步骤4 - 拼接所有行并返回
    pass


# ===== 测试 =====
if __name__ == "__main__":
    # 测试 format_info
    result = format_info("Alice", "Bob", city="北京", age=25)
    print(f"测试1: {result}")
    # 期望: "人员: Alice, Bob | 附加信息: city=北京, age=25"
    
    result2 = format_info("张三")
    print(f"测试2: {result2}")
    # 期望: "人员: 张三 | 附加信息: 无"
    
    result3 = format_info()
    print(f"测试3: {result3}")
    # 期望: "人员: 无 | 附加信息: 无"
    
    # 测试 format_table
    table = format_table("姓名", "年龄", "城市",
                         rows=[("Alice", 25, "北京"), ("Bob", 30, "上海")])
    print(f"\n测试4 - 表格:\n{table}")
