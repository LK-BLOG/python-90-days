# Day 5 挑战一：推导式大师 (★☆☆☆☆)
# 难度: ★☆☆☆☆
# 要求: 熟练掌握列表推导式、字典推导式、集合推导式。


# ===== 任务1: 列表推导式 =====
numbers = list(range(1, 21))  # [1, 2, 3, ..., 20]

# TODO: 生成偶数的平方列表
even_squares = [x ** 2 for x in numbers if x % 2 == 0]
print(f"偶数平方: {even_squares}")
# 期望: [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

# TODO: 生成 (数字, 平方) 元组列表
pairs = [(x, x ** 2) for x in numbers[:5]]
print(f"数字-平方对: {pairs}")

# TODO: 嵌套推导式 —— 生成乘法表数据
multiplication = [(i, j, i * j) for i in range(1, 10) for j in range(1, i + 1)]
print(f"乘法表前3项: {multiplication[:3]}")

# ===== 任务2: 字典推导式 =====
words = ["hello", "world", "python", "ai"]

# TODO: 单词 -> 长度 的字典
word_lens = {w: len(w) for w in words}
print(f"单词长度: {word_lens}")

# TODO: 反转字典 {长度: [单词列表]}
length_to_words = {}
for w in words:
    length_to_words.setdefault(len(w), []).append(w)
# 用推导式重写（提示：可能需要配合 defaultdict 或 setdefault）
print(f"按长度分组: {length_to_words}")

# ===== 任务3: 集合推导式 =====
text = "hello world python programming"

# TODO: 提取所有唯一字符（不包括空格）
unique_chars = {c for c in text if c != ' '}
print(f"唯一字符: {sorted(unique_chars)}")

# TODO: 生成所有两位数的质数集合
primes = {n for n in range(10, 100) if all(n % i != 0 for i in range(2, int(n**0.5) + 1))}
print(f"两位数质数 ({len(primes)}个): {sorted(primes)[:10]}...")

# ===== 任务4: 生成器表达式 =====
# TODO: 用生成器表达式求大列表的和（内存友好）
big_numbers = range(1_000_000)
total = sum(x ** 2 for x in big_numbers if x % 3 == 0)
print(f"\n100万内3的倍数的平方和: {total}")


# ===== 扩展挑战 =====
def flatten_matrix(matrix):
    """用推导式展平二维矩阵。
    
    Args:
        matrix: 二维列表 [[1,2],[3,4],[5,6]]
    
    Returns:
        list: [1,2,3,4,5,6]
    """
    # TODO: 使用嵌套列表推导式
    pass


def zip_dict(keys, values):
    """用推导式将两个列表合并为字典（过滤 None 值）。
    
    Args:
        keys: 键列表
        values: 值列表
    
    Returns:
        dict: 过滤掉值为 None 的字典
    """
    # TODO: 使用字典推导式 + zip + 条件过滤
    pass


# ===== 测试 =====
if __name__ == "__main__":
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"\n展平: {flatten_matrix(matrix)}")
    
    keys = ["a", "b", "c", "d"]
    values = [1, None, 3, None]
    print(f"过滤字典: {zip_dict(keys, values)}")
