# Day 5: 数据结构进阶 — 完整教学

---

## 1. 列表推导式

### 示例
```python
# 基础
squares = [x ** 2 for x in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 带条件
evens = [x for x in range(20) if x % 2 == 0]
print(evens)

# if-else（注意位置不同！）
result = [x if x > 0 else 0 for x in [-1, 2, -3, 4]]
print(result)  # [0, 2, 0, 4]

# 嵌套循环
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
print(pairs)

# 嵌套列表展开
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 常见错误
```python
# if-else位置错误
# [x for x in range(10) if x > 5 else 0]  # SyntaxError
# 正确：if-else在for前面
result = [x if x > 5 else 0 for x in range(10)]
```

---

## 2. 字典推导式

### 示例
```python
# 基础
sq_dict = {x: x**2 for x in range(1, 6)}
print(sq_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 反转字典
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # {1: 'a', 2: 'b', 3: 'c'}

# 带条件过滤
scores = {"张三": 85, "李四": 92, "王五": 78, "赵六": 95}
excellent = {k: v for k, v in scores.items() if v >= 90}
print(excellent)  # {'李四': 92, '赵六': 95}
```

---

## 3. 集合推导式

### 示例
```python
words = ["hello", "world", "python", "hello", "world"]
unique_lengths = {len(w) for w in words}
print(unique_lengths)  # {5, 6}

# 去重 + 转换
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x ** 2 for x in data}
print(unique_squares)  # {16, 1, 4, 9}
```

---

## 4. 嵌套数据结构操作

### 示例
```python
# 嵌套字典
students = {
    "张三": {"age": 20, "scores": [85, 90, 78]},
    "李四": {"age": 22, "scores": [92, 88, 95]},
    "王五": {"age": 19, "scores": [78, 82, 80]},
}

# 获取嵌套值
print(students["张三"]["scores"][0])  # 85

# 列表推导式处理嵌套
averages = {
    name: sum(s["scores"]) / len(s["scores"])
    for name, s in students.items()
}
print(averages)

# 扁平化嵌套结构
nested = {"a": [1, 2], "b": [3, 4], "c": [5, 6]}
flat = [item for sublist in nested.values() for item in sublist]
print(flat)  # [1, 2, 3, 4, 5, 6]
```

---

## 5. enumerate 和 zip

### 示例
```python
# enumerate — 带索引遍历
fruits = ["苹果", "香蕉", "橘子"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip — 并行遍历
names = ["张三", "李四", "王五"]
ages = [25, 30, 22]
cities = ["北京", "上海", "广州"]

for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age}岁, {city}")

# zip转字典
name_age = dict(zip(names, ages))
print(name_age)  # {'张三': 25, '李四': 30, '王五': 22}

# unzip（反向zip）
pairs = [("a", 1), ("b", 2), ("c", 3)]
keys, values = zip(*pairs)
print(keys)   # ('a', 'b', 'c')
print(values) # (1, 2, 3)
```

---

## 6. collections 模块

### Counter — 计数器
```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counter = Counter(words)
print(counter)          # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(counter.most_common(2))  # [('apple', 3), ('banana', 2)]

# 字符频率统计
text = "hello world"
char_count = Counter(text)
print(char_count)       # Counter({'l': 3, 'o': 2, 'h': 1, ...})
```

### defaultdict — 默认字典
```python
from collections import defaultdict

# 按类别分组
items = [("水果", "苹果"), ("蔬菜", "白菜"), ("水果", "香蕉"), ("蔬菜", "萝卜")]
grouped = defaultdict(list)
for category, item in items:
    grouped[category].append(item)
print(dict(grouped))  # {'水果': ['苹果', '香蕉'], '蔬菜': ['白菜', '萝卜']}

# 计数
word_count = defaultdict(int)
for word in ["hello", "world", "hello", "python"]:
    word_count[word] += 1
print(dict(word_count))  # {'hello': 2, 'world': 1, 'python': 1}
```

### deque — 双端队列
```python
from collections import deque

dq = deque([1, 2, 3])
dq.appendleft(0)   # [0, 1, 2, 3]
dq.append(4)       # [0, 1, 2, 3, 4]
dq.popleft()        # 0, 队列变为 [1, 2, 3, 4]

# 固定长度的历史记录
history = deque(maxlen=3)
for cmd in ["ls", "cd", "pwd", "cat"]:
    history.append(cmd)
print(history)  # deque(['cd', 'pwd', 'cat'])
```

### namedtuple — 命名元组
```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)    # 3 4
print(p[0], p[1])  # 3 4（也支持索引）

# 比普通字典更轻量
Student = namedtuple("Student", "name age score")
s = Student("张三", 20, 85)
print(f"{s.name} 得了 {s.score} 分")
```

---

## 总结

| 技术 | 用途 |
|------|------|
| 列表推导式 | 快速创建/转换列表 |
| 字典推导式 | 快速创建字典 |
| 集合推导式 | 去重、集合操作 |
| enumerate | 带索引遍历 |
| zip | 并行遍历 |
| Counter | 计数统计 |
| defaultdict | 自动初始化字典 |
| deque | 高效双端操作 |
| namedtuple | 带名称的元组 |
