# Day 5 挑战二：数据分组器 (★★☆☆☆)
# 难度: ★★☆☆☆
# 要求: 实现各种数据分组和聚合操作。


from collections import defaultdict, Counter


# ===== 测试数据 =====
students = [
    {"name": "Alice", "age": 22, "grade": "A", "major": "CS"},
    {"name": "Bob", "age": 21, "grade": "B", "major": "Math"},
    {"name": "Charlie", "age": 23, "grade": "A", "major": "CS"},
    {"name": "Diana", "age": 22, "grade": "B", "major": "Math"},
    {"name": "Eve", "age": 21, "grade": "A", "major": "CS"},
    {"name": "Frank", "age": 24, "grade": "C", "major": "Physics"},
]


def group_by(items, key_func):
    """通用分组函数 —— 按指定键将数据分组。
    
    功能说明:
        类似 SQL 的 GROUP BY，将列表中的元素按 key_func 的返回值分组。
    
    示例:
        >>> group_by(students, lambda s: s["grade"])
        {"A": [Alice, Charlie, Eve], "B": [Bob, Diana], "C": [Frank]}
    
    Args:
        items: 数据列表
        key_func: 分组键函数，接收元素返回分组键
    
    Returns:
        dict: {分组键: [元素列表]}
    """
    # TODO: 使用 defaultdict 或推导式实现分组
    pass


def group_by_multiple(items, *key_funcs):
    """多级分组 —— 按多个键依次分组。
    
    功能说明:
        先按第一个 key_func 分组，再对每个子组按第二个 key_func 分组。
    
    示例:
        >>> group_by_multiple(students, 
        ...     lambda s: s["grade"],
        ...     lambda s: s["major"])
        {"A": {"CS": [Alice, Charlie, Eve], ...}, "B": {...}}
    
    Args:
        items: 数据列表
        *key_funcs: 多个分组键函数
    
    Returns:
        dict: 嵌套的分组字典
    """
    # TODO: 递归实现多级分组
    pass


def aggregate(items, group_key, agg_key, agg_func):
    """分组聚合 —— 先分组，再对每组的某个字段做聚合。
    
    示例:
        >>> aggregate(students, "major", "age", lambda ages: sum(ages)/len(ages))
        {"CS": 22.33, "Math": 21.5, "Physics": 24.0}
    
    Args:
        items: 数据列表
        group_key: 分组键
        agg_key: 聚合字段
        agg_func: 聚合函数
    
    Returns:
        dict: {分组键: 聚合结果}
    """
    # TODO: 先 group_by，再对每组应用 agg_func
    pass


def pivot_table(data, rows_key, cols_key, value_key, agg_func=sum):
    """简单的数据透视表。
    
    功能说明:
        按行键和列键生成交叉表，值通过 agg_func 聚合。
    
    Args:
        data: 字典列表
        rows_key: 行键字段名
        cols_key: 列键字段名
        value_key: 值字段名
        agg_func: 聚合函数
    
    Returns:
        dict: {行键: {列键: 聚合值}}
    """
    # TODO: 使用嵌套 defaultdict 实现透视
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("=== 按年级分组 ===")
    by_grade = group_by(students, lambda s: s["grade"])
    for grade, group in by_grade.items():
        names = [s["name"] for s in group]
        print(f"  {grade}: {names}")
    
    print("\n=== 按专业平均年龄 ===")
    avg_age = aggregate(students, "major", "age",
                       lambda ages: round(sum(ages) / len(ages), 1))
    for major, age in avg_age.items():
        print(f"  {major}: {age}")
    
    print("\n=== 透视表 ===")
    sales = [
        {"region": "北", "product": "A", "amount": 100},
        {"region": "北", "product": "B", "amount": 200},
        {"region": "南", "product": "A", "amount": 150},
        {"region": "南", "product": "B", "amount": 180},
    ]
    pivot = pivot_table(sales, "region", "product", "amount")
    for region, products in pivot.items():
        print(f"  {region}: {products}")
