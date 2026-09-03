# Day 2: 函数高级 — 完整教学

---

## 1. 函数作为变量赋值

### 说明
在Python中，函数是一等公民，可以像普通变量一样赋值、传递、存储。

### 示例
```python
def greet(name):
    return f"你好, {name}!"

say_hello = greet
print(say_hello("小明"))  # 你好, 小明!

# 函数在数据结构中
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
}
print(operations["add"](3, 5))  # 8
```

### 常见错误
```python
def get_value():
    return 42
result = get_value   # 错！这是函数对象
print(result())      # 42 — 这才是调用
```

---

## 2. 高阶函数

### 说明
高阶函数是接收函数作为参数或返回函数的函数。

### 示例
```python
def apply_twice(func, value):
    return func(func(value))

def add_five(x):
    return x + 5

print(apply_twice(add_five, 10))  # 20
```

---

## 3. lambda 表达式

### 说明
lambda是匿名函数，适合简短的一次性使用。

### 示例
```python
square = lambda x: x ** 2
print(square(5))  # 25

students = [("张三", 85), ("李四", 92), ("王五", 78)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(by_score)
```

---

## 4. map() 和 filter()

### 示例
```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

evens = list(filter(lambda x: x % 2 == 0, range(1, 11)))
print(evens)  # [2, 4, 6, 8, 10]
```

### 常见错误
```python
result = map(lambda x: x * 2, [1, 2, 3])
print(result)       # <map object> — 需要转list
print(list(result)) # [2, 4, 6]
```

---

## 5. sorted() 深入

### 示例
```python
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print(by_score)
```

---

## 6. 函数返回函数（工厂函数）

### 示例
```python
def multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
```

### 常见错误：闭包延迟绑定
```python
functions = []
for i in range(5):
    functions.append(lambda: i)
print([f() for f in functions])  # [4, 4, 4, 4, 4]!

# 解决：
functions = []
for i in range(5):
    functions.append(lambda i=i: i)
print([f() for f in functions])  # [0, 1, 2, 3, 4]
```

---

## 7. partial 偏函数

### 示例
```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5))  # 25
print(cube(5))    # 125

binary_to_int = partial(int, base=2)
print(binary_to_int("1010"))  # 10
```

---

## 总结

| 概念 | 说明 |
|------|------|
| 函数赋值 | 函数赋值给变量 |
| 高阶函数 | 函数作为参数/返回值 |
| lambda | 匿名函数 |
| map/filter | 批量转换/筛选 |
| sorted+key | 自定义排序 |
| 工厂函数 | 返回函数的函数 |
| partial | 固定部分参数 |

---

## 4. map() 和 filter()

### 说明
- `map(func, iterable)`：对每个元素应用函数，返回迭代器
- `filter(func, iterable)`：筛选满足条件的元素，返回迭代器

### 语法
```python
result = map(函数, 可迭代对象)
result = filter(函数, 可迭代对象)
```

### 示例
```python
# map — 转换
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# 多个可迭代对象
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)  # [11, 22, 33]

# map + 类型转换（常用！）
str_numbers = ["1", "2", "3", "4", "5"]
int_numbers = list(map(int, str_numbers))
print(int_numbers)  # [1, 2, 3, 4, 5]

# filter — 筛选
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# filter(None, ...) 去除假值
data = [0, 1, "", "hello", None, [], [1], False, True]
truthy = list(filter(None, data))
print(truthy)  # [1, 'hello', [1], True]
```

### 常见错误
```python
# map返回的是迭代器，不是列表！
result = map(lambda x: x * 2, [1, 2, 3])
print(result)   # <map object at 0x...>
print(list(result))  # [2, 4, 6] — 需要转list

# map只能迭代一次！
result = map(lambda x: x * 2, [1, 2, 3])
print(list(result))  # [2, 4, 6]
print(list(result))  # [] — 空了！
```

### 实际应用
```python
# 批量处理数据
names = ["  张三  ", " 李四 ", "王五  "]
cleaned = list(map(str.strip, names))
print(cleaned)  # ['张三', '李四', '王五']

# 筛选有效数据
records = [
    {"name": "张三", "age": 25},
    {"name": "", "age": 30},
    {"name": "王五", "age": -1},
    {"name": "李四", "age": 22},
]
valid = list(filter(lambda r: r["name"] and r["age"] > 0, records))
print(valid)
```

### 动手练习
```python
words = ["Hello", "World", "Python", "Is", "Great"]
# 用map获取所有单词的小写形式
# TODO
lower_words = None
print(lower_words)

# 用filter筛选长度大于3的单词
# TODO
long_words = None
print(long_words)
```

---

## 5. sorted() 深入

### 说明
sorted() 是内置排序函数，支持 `key` 参数自定义排序规则。

### 语法
```python
sorted(可迭代对象, key=函数, reverse=False)
```

### 示例
```python
# 基础排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(numbers))           # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(numbers, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]

# 字符串排序
words = ["banana", "apple", "cherry", "date"]
print(sorted(words))  # ['apple', 'banana', 'cherry', 'date']
print(sorted(words, key=len))  # ['date', 'apple', 'banana', 'cherry']

# 字典列表排序
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
for s in by_score:
    print(f"{s['name']}: {s['score']}")
# 李四: 92, 张三: 85, 王五: 78

# 多级排序
data = [("张三", 90), ("李四", 85), ("王五", 90), ("赵六", 85)]
result = sorted(data, key=lambda x: (-x[1], x[0]))
print(result)  # [('张三', 90), ('王五', 90), ('李四', 85), ('赵六', 85)]

# 用 operator.itemgetter（比lambda更快）
from operator import itemgetter
result = sorted(students, key=itemgetter("score"), reverse=True)

# 用 operator.attrgetter 排序对象
```

---

## 6. 函数返回函数（工厂函数）

### 说明
函数可以返回另一个函数，这是实现闭包和装饰器的基础。

### 语法
```python
def 外部函数(配置参数):
    def 内部函数(运行参数):
        # 使用配置参数和运行参数
        return 结果
    return 内部函数
```

### 示例
```python
# 生成不同倍数的函数
def multiplier(n):
    """返回一个乘以n的函数"""
    def multiply(x):
        return x * n
    return multiply

double = multiplier(2)
triple = multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# 生成比较函数
def compare_by(key):
    """返回按指定key排序的比较函数"""
    return lambda item: item[key]

users = [{"name": "张三", "age": 30}, {"name": "李四", "age": 25}]
by_age = sorted(users, key=compare_by("age"))
print(by_age)  # 按age排序

# 生成验证器
def make_validator(min_val, max_val):
    def validate(value):
        return min_val <= value <= max_val
    return validate

age_check = make_validator(0, 150)
print(age_check(25))   # True
print(age_check(200))  # False
```

### 常见错误
```python
# 闭包中的延迟绑定问题
functions = []
for i in range(5):
    functions.append(lambda: i)  # lambda捕获的是变量i，不是值

print([f() for f in functions])  # [4, 4, 4, 4, 4] — 不是 [0, 1, 2, 3, 4]！

# 解决方案：用默认参数绑定当前值
functions = []
for i in range(5):
    functions.append(lambda i=i: i)  # 默认参数在定义时求值

print([f() for f in functions])  # [0, 1, 2, 3, 4]
```

### 实际应用
```python
# 生成不同格式的格式化器
def make_formatter(template):
    def formatter(data):
        return template.format(**data)
    return formatter

json_fmt = make_formatter('{"name": "{name}", "age": {age}}')
csv_fmt = make_formatter("{name},{age}")
xml_fmt = make_formatter("<user><name>{name}</name><age>{age}</age></user>")

data = {"name": "张三", "age": 25}
print(json_fmt(data))
print(csv_fmt(data))
print(xml_fmt(data))
```

---

## 7. partial 偏函数

### 说明
`functools.partial` 固定函数的部分参数，生成一个新函数。

### 语法
```python
from functools import partial
新函数 = partial(原函数, 固定参数...)
```

### 示例
```python
from functools import partial

# 固定部分参数
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# 实用场景：int的偏函数
binary_to_int = partial(int, base=2)
hex_to_int = partial(int, base=16)

print(binary_to_int("1010"))   # 10
print(hex_to_int("ff"))        # 255

# 简化函数调用
def send_request(url, method="GET", timeout=30, headers=None):
    print(f"{method} {url} timeout={timeout}")

# 创建常用配置的快捷方式
post_json = partial(send_request, method="POST", headers={"Content-Type": "application/json"})
post_json("https://api.example.com/data", timeout=60)
```

### 实际应用
```python
from functools import partial

# 批量处理中的应用
def parse_date(date_string, fmt="%Y-%m-%d"):
    from datetime import datetime
    return datetime.strptime(date_string, fmt)

# 常用格式的快捷方式
parse_iso = partial(parse_date, fmt="%Y-%m-%d")
parse_us = partial(parse_date, fmt="%m/%d/%Y")
parse_cn = partial(parse_date, fmt="%Y年%m月%d日")

print(parse_iso("2024-01-15"))
print(parse_cn("2024年01月15日"))
```

---

## 总结

| 概念 | 说明 | 使用场景 |
|------|------|----------|
| 函数赋值 | 函数赋值给变量 | 动态分发、策略选择 |
| 高阶函数 | 函数作为参数/返回值 | 回调、策略模式 |
| lambda | 匿名函数 | 排序key、简单转换 |
| map/filter | 批量转换/筛选 | 数据处理管道 |
| sorted+key | 自定义排序 | 列表/字典排序 |
| 工厂函数 | 返回函数的函数 | 闭包、装饰器 |
| partial | 固定部分参数 | 创建快捷函数 |
