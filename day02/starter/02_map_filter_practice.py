# -*- coding: utf-8 -*-
# Day 2 挑战二：Map-Filter链 (★★☆☆☆)
# 难度: ★★☆☆☆
# 要求: 用 map 和 filter 处理列表数据。

# ===== 测试数据 =====
words = ["Hello", "World", "Python", "Is", "Great", "AI"]
numbers = list(range(1, 21))  # [1, 2, 3, ..., 20]

# ===== 任务1: Map 基础 =====
# TODO: 用 map 将所有单词转为小写
lower_words = list(map(lambda w: w.lower(), words))  # 基础示例，可直接运行
print(f"小写: {lower_words}")

# TODO: 用 map 计算每个数字的平方
squares = list(map(lambda x: x ** 2, numbers[:5]))
print(f"平方: {squares}")

# TODO: 用 map 计算每个单词的长度
word_lengths = list(map(lambda w: len(w), words))
print(f"长度: {list(zip(words, word_lengths))}")

# ===== 任务2: Filter 基础 =====
# TODO: 筛选长度 > 3 的单词
long_words = list(filter(lambda w: len(w) > 3, words))
print(f"长单词: {long_words}")

# TODO: 筛选偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

# TODO: 筛选以 'A' 或 'a' 开头的单词
a_words = list(filter(lambda w: w.lower().startswith("a"), words))
print(f"A开头: {a_words}")

# ===== 任务3: Map-Filter 链式组合 =====
# TODO: 筛选偶数 -> 计算平方 -> 求和
result = sum(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
print(f"偶数平方和: {result}")

# TODO: 筛选长度>3的单词 -> 转大写 -> 按字母排序
result_words = sorted(map(lambda w: w.upper(), filter(lambda w: len(w) > 3, words)))
print(f"大写长单词: {result_words}")


# ===== 扩展挑战 =====
def pipeline(*functions):
    """函数管道组合器。
    
    功能说明:
        将多个函数组合成一个管道，数据从左到右依次流过每个函数。
    
    示例:
        transform = pipeline(
            lambda x: x * 2,
            lambda x: x + 10,
            lambda x: x ** 2
        )
        transform(3)  # ((3*2)+10)^2 = 256
    
    Args:
        *functions: 任意数量的函数（每个函数接收一个参数，返回一个值）
    
    Returns:
        callable: 组合后的函数
    """
    # TODO: 使用 reduce 或循环实现函数组合
    # 提示: 管道中前一个函数的输出是下一个函数的输入
    pass


def compose(*functions):
    """反向函数组合（从右到左执行）。
    
    功能说明:
        数学意义上的函数组合 f(g(h(x)))。
    
    Args:
        *functions: 从右到左执行的函数序列
    
    Returns:
        callable: 组合后的函数
    """
    # TODO: 实现反向组合
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("\n=== pipeline 测试 ===")
    double_then_add = pipeline(lambda x: x * 2, lambda x: x + 10)
    print(f"pipeline(3) = {double_then_add(3)}")  # 期望: 16
    
    print("\n=== compose 测试 ===")
    # compose(f, g)(x) = f(g(x))
    add_then_double = compose(lambda x: x * 2, lambda x: x + 10)
    print(f"compose(3) = {add_then_double(3)}")  # 期望: 26
