# -*- coding: utf-8 -*-
# Day 2 挑战一：排序大师 (★☆☆☆☆)
# 难度: ★☆☆☆☆
# 要求: 用 sorted 和 lambda 对复杂数据进行多级排序。

# ===== 测试数据 =====
students = [
    {"name": "张三", "age": 20, "score": 85, "city": "北京"},
    {"name": "李四", "age": 22, "score": 92, "city": "上海"},
    {"name": "王五", "age": 19, "score": 78, "city": "北京"},
    {"name": "赵六", "age": 21, "score": 92, "city": "广州"},
    {"name": "孙七", "age": 20, "score": 85, "city": "上海"},
]

# ===== 任务 =====

# 任务1: 按分数降序排列
by_score_desc = sorted(students, key=lambda s: s["score"], reverse=True)
print("按分数降序:")
for s in by_score_desc:
    print(f"  {s['name']}: {s['score']}")

# 任务2: 先按城市升序，再按分数降序（多级排序）
by_city_score = sorted(students, key=lambda s: (s["city"], -s["score"]))
print("\n按城市+分数排序:")
for s in by_city_score:
    print(f"  {s['city']} | {s['name']}: {s['score']}")

# 任务3: 按年龄升序，年龄相同按名字排序
# TODO: 用 sorted + lambda 实现
by_age_name = None  # TODO: 替换为 sorted(...)
print("\n按年龄+名字排序:")
if by_age_name:
    for s in by_age_name:
        print(f"  {s['age']}岁 | {s['name']}")

# 任务4: 提取并排序分数列表（去重后降序）
# TODO: 用 sorted + set + lambda 实现
unique_scores = None  # TODO: 替换
print(f"\n去重分数降序: {unique_scores}")

# 任务5: 自定义排序 - 按字符串长度排序
words = ["Python", "Go", "JavaScript", "Rust", "C", "TypeScript"]
# TODO: 按字符串长度升序排序
by_length = None  # TODO: 替换
print(f"\n按长度排序: {by_length}")


# ===== 扩展挑战 =====
def multi_sort(data, *key_funcs, reverse=False):
    """通用多级排序函数。
    
    功能说明:
        接收数据和多个排序键函数，按优先级依次排序。
    
    示例:
        result = multi_sort(students,
            lambda s: s["city"],
            lambda s: -s["score"]
        )
    
    Args:
        data: 待排序的可迭代对象
        *key_funcs: 排序键函数（按优先级排列）
        reverse: 是否反转排序结果
    
    Returns:
        list: 排序后的新列表
    """
    # TODO: 实现多级排序
    # 提示: 使用 tuple 作为复合键
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("\n=== multi_sort 测试 ===")
    result = multi_sort(students,
                        lambda s: s["city"],
                        lambda s: -s["score"])
    if result:
        for s in result:
            print(f"  {s['city']} | {s['name']}: {s['score']}")
