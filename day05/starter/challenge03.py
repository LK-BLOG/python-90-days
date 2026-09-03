# Day 5 挑战三：collections 玩家 (★★★☆☆)
# 难度: ★★★☆☆
# 要求: 深入掌握 collections 模块的各种数据结构。


from collections import (
    Counter, OrderedDict, defaultdict,
    namedtuple, deque, ChainMap
)


# ===== 任务1: Counter 计数器 =====
text = "the quick brown fox jumps over the lazy dog the fox"

# TODO: 统计词频
word_count = Counter(text.split())
print("词频统计:")
for word, count in word_count.most_common(5):
    print(f"  {word}: {count}")

# TODO: 合并两个 Counter
a = Counter(apples=3, bananas=2)
b = Counter(apples=1, bananas=5, oranges=3)
# 用 + 合并
merged = a + b
print(f"\n合并: {merged}")

# TODO: 用 Counter 找出列表中出现次数超过一半的元素
data = [1, 2, 3, 1, 2, 1, 1, 4, 1]
majority = None  # TODO: 用 Counter 找出出现次数最多的元素
print(f"多数元素: {majority}")


# ===== 任务2: defaultdict 默认字典 =====
# TODO: 按首字母分组
words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
by_first_letter = defaultdict(list)
# TODO: 填充数据
for w in words:
    by_first_letter[w[0]].append(w)
print(f"\n按首字母分组: {dict(by_first_letter)}")

# TODO: 用 defaultdict 统计嵌套数据
votes = [
    ("Alice", "Python"), ("Bob", "Java"), ("Alice", "Java"),
    ("Charlie", "Python"), ("Bob", "Python"), ("Diana", "Java"),
]
candidate_votes = defaultdict(lambda: defaultdict(int))
for voter, candidate in votes:
    # TODO: 统计每个候选人的票数
    pass
print(f"\n投票统计: {dict(candidate_votes)}")


# ===== 任务3: deque 双端队列 =====
# TODO: 实现一个固定大小的最近记录（滑动窗口）
class RecentRecords:
    """最近 N 条记录的滑动窗口。"""
    
    def __init__(self, maxlen=10):
        # TODO: 使用 deque 初始化
        pass
    
    def add(self, record):
        """添加一条记录，超过 maxlen 时自动丢弃最旧的。"""
        # TODO: append 到 deque
        pass
    
    def get_latest(self, n=None):
        """获取最近 n 条记录。"""
        # TODO: 返回 deque 的最后 n 个元素
        pass
    
    def __len__(self):
        pass
    
    def __iter__(self):
        pass


# ===== 任务4: namedtuple 命名元组 =====
# TODO: 定义一个 Point 命名元组
Point = namedtuple("Point", ["x", "y"])  # 已定义

# TODO: 定义一个更复杂的命名元组
Stock = namedtuple("Stock", ["symbol", "price", "volume", "change"])  # TODO: 填充

# TODO: 用 _make 和 _asdict
p = Point._make([3, 4])  # TODO: 理解 _make 的用法
print(f"\nPoint: {p}, 距原点距离: {(p.x**2 + p.y**2)**0.5:.2f}")


# ===== 任务5: OrderedDict 有序字典 =====
# TODO: 实现一个 LRU 缓存（使用 OrderedDict）
class LRUCache:
    """最近最少使用缓存。"""
    
    def __init__(self, capacity):
        # TODO: 使用 OrderedDict 初始化
        pass
    
    def get(self, key):
        """获取缓存值，命中时移到末尾。"""
        # TODO: 实现 get 逻辑
        pass
    
    def put(self, key, value):
        """设置缓存值，满时淘汰最旧的。"""
        # TODO: 实现 put 逻辑
        pass


# ===== 测试 =====
if __name__ == "__main__":
    print("\n=== RecentRecords ===")
    rr = RecentRecords(maxlen=3)
    for i in range(5):
        rr.add(f"record_{i}")
    print(f"最新3条: {list(rr.get_latest(3))}")
    
    print("\n=== LRUCache ===")
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(f"get a: {cache.get('a')}")
    cache.put("d", 4)  # 应该淘汰 b
    print(f"get b: {cache.get('b')}")  # 期望 None
    print(f"get d: {cache.get('d')}")
