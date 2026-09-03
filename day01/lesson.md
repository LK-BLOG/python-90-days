# Day 1: 函数参数 — 完整教学

---

## 1. 位置参数

### 说明
位置参数是最基本的参数类型，调用时必须按顺序提供，数量必须匹配。

### 语法
```python
def 函数名(参数1, 参数2, ...):
    函数体
```

### 示例
```python
# 定义一个函数，接收两个位置参数
def greet(name, age):
    print(f"你好，我叫{name}，今年{age}岁")

# 正确调用：按顺序传入
greet("小明", 25)   # 输出：你好，我叫小明，今年25岁

# 顺序错误 — 逻辑bug
greet(25, "小明")    # 输出：你好，我叫25，今年小明岁

# 参数数量不对
# greet("小明")      # TypeError: missing 1 required positional argument
```

### 常见错误
1. **参数数量不匹配**：调用时少传或多传参数
2. **顺序搞混**：尤其参数类型相同时容易传反
3. **忘记参数**：调用时遗漏某个参数

### 实际应用
```python
# 文件操作 — 位置参数很自然
def save_data(filename, data, encoding="utf-8"):
    with open(filename, "w", encoding=encoding) as f:
        f.write(data)
```

### 动手练习
```python
# 修改下面的函数，使其接收姓名和城市两个参数，并打印问候语
def greet_person():
    pass

# 测试：应该输出 "欢迎来到北京的张三！"
greet_person("张三", "北京")
```

---

## 2. 关键字参数

### 说明
关键字参数在调用时通过"参数名=值"的方式传入，顺序无所谓。

### 语法
```python
函数名(参数名1=值1, 参数名2=值2)
```

### 示例
```python
def greet(name, age):
    print(f"你好，我叫{name}，今年{age}岁")

# 关键字调用，顺序随意
greet(age=25, name="小明")  # 正确
greet(name="小明", age=25)  # 同样正确

# 混合使用：位置参数必须在关键字参数前面
greet("小明", age=25)        # 正确
# greet(name="小明", 25)    # SyntaxError
```

### 常见错误
1. **位置参数放在关键字参数后面**：报 SyntaxError
2. **重复传值**：同一个参数传了两次报 TypeError
3. **拼错参数名**：报 TypeError: unexpected keyword argument

### 实际应用
```python
def create_user(name, email, role="viewer", active=True, department=None):
    return {"name": name, "email": email, "role": role, "active": active, "dept": department}

# 只传必须的，其余用默认值
user = create_user("张三", "zhangsan@example.com", role="admin", department="技术部")
```

### 动手练习
```python
def create_user(name, email, role="viewer", active=True):
    return {"name": name, "email": email, "role": role, "active": active}

# TODO: 用关键字参数调用，创建一个名为"李四"的管理员
user = None  # 替换为你的调用
print(user)
```

---

## 3. 默认参数

### 说明
默认参数在定义时给定默认值，调用时可以不传，会使用默认值。

### 语法
```python
def 函数名(参数=默认值):
    函数体
```

### 示例
```python
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}")

greet("小明")            # 输出：你好，小明
greet("小明", "早上好")   # 输出：早上好，小明

# 默认参数必须放在非默认参数后面
# def greet(greeting="你好", name):  # SyntaxError
```

### 常见错误（重点！）
```python
# 经典坑：可变对象作为默认参数
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b'] — 不是['b']！
# 原因：默认参数在函数定义时就创建了，不会每次调用重新创建

# 正确做法：
def add_item_safe(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 实际应用
```python
def connect_db(host="localhost", port=3306, user="root", password="", db="test"):
    print(f"连接到 {host}:{port}/{db} 用户:{user}")
    return {"host": host, "port": port, "user": user, "db": db}

conn = connect_db()                                    # 用默认值
conn = connect_db(host="192.168.1.100", db="production") # 覆盖部分
```

### 动手练习
```python
# 修复下面函数的默认参数问题
def append_number(num, result=[]):
    result.append(num)
    return result

# 预期：第一次返回[1]，第二次返回[2]
print(append_number(1))
print(append_number(2))
```

---

## 4. 参数传递（可变 vs 不可变）

### 说明
Python传参是"传对象引用"。不可变对象（int, str, tuple）在函数内修改会创建新对象；可变对象（list, dict, set）在函数内修改会影响外部。

### 语法
无特殊语法，由参数类型决定。

### 示例
```python
# 不可变参数 — 函数内修改不影响外部
def change_num(n):
    n = 100

x = 5
change_num(x)
print(x)  # 5 — 没变

# 可变参数 — 函数内修改会影响外部！
def change_list(lst):
    lst.append(4)

my_list = [1, 2, 3]
change_list(my_list)
print(my_list)  # [1, 2, 3, 4] — 变了！

# 但是重新赋值不影响外部
def reassign_list(lst):
    lst = [999, 888]

my_list = [1, 2, 3]
reassign_list(my_list)
print(my_list)  # [1, 2, 3] — 没变
```

### 常见错误
```python
# 以为传了不可变对象就安全，结果传了个包含可变对象的tuple
def dangerous(tup):
    tup[0].append(999)

t = ([1, 2], "hello")
dangerous(t)
print(t)  # ([1, 2, 999], 'hello') — 惊不惊喜？
```

### 实际应用
```python
# 不想让函数修改原始数据？传副本
def sort_and_return(lst):
    sorted_lst = sorted(lst)  # sorted返回新列表
    return sorted_lst

original = [3, 1, 2]
result = sort_and_return(original)
print(original)  # [3, 1, 2] — 没变
print(result)    # [1, 2, 3]
```

### 动手练习
```python
def mystery(a, b):
    a.append(4)
    b = b + [4]
    return a, b

x = [1, 2, 3]
y = [1, 2, 3]
x2, y2 = mystery(x, y)
# TODO: print x, y, x2, y2 分别是什么？先猜再运行
print("x =", x)
print("y =", y)
print("x2 =", x2)
print("y2 =", y2)
```

---

## 5. *args — 可变位置参数

### 说明
`*args` 让函数接收任意数量的位置参数，打包成一个元组。

### 语法
```python
def 函数名(普通参数, *args):
    函数体
# 调用时：函数名(1, 2, 3, 4, 5)
# args = (2, 3, 4, 5)
```

### 示例
```python
def calculate_sum(*numbers):
    """接收任意个数字，返回总和"""
    total = 0
    for num in numbers:
        total += num
    return total

print(calculate_sum(1, 2, 3))       # 6
print(calculate_sum(1, 2, 3, 4, 5))  # 15
print(calculate_sum())                # 0

# 混合使用
def func(a, b, *args):
    print(f"a={a}, b={b}, args={args}")

func(1, 2, 3, 4, 5)  # a=1, b=2, args=(3, 4, 5)
```

### 常见错误
```python
# args永远是tuple，不能修改元素
def buggy(*args):
    args[0] = 999  # TypeError: 'tuple' does not support item assignment

# args必须放在普通参数后面
# def buggy(*args, a, b):  # SyntaxError
```

### 实际应用
```python
def log(*messages, level="INFO"):
    for msg in messages:
        print(f"[{level}] {msg}")

log("用户登录", "访问首页", "查看订单", level="DEBUG")
```

### 动手练习
```python
# 实现一个函数，接收任意数量的字符串，返回用空格连接的结果
def join_strings(*strings):
    # TODO
    pass

print(join_strings("hello", "world"))      # "hello world"
print(join_strings("a", "b", "c", "d"))     # "a b c d"
```

---

## 6. **kwargs — 可变关键字参数

### 说明
`**kwargs` 让函数接收任意数量的关键字参数，打包成一个字典。

### 语法
```python
def 函数名(普通参数, **kwargs):
    函数体
# 调用时：func(name="张三", age=25)
# kwargs = {"name": "张三", "age": 25}
```

### 示例
```python
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="张三", age=25, city="北京")

# 混合使用
def func(a, b, *args, **kwargs):
    print(f"a={a}, b={b}, args={args}, kwargs={kwargs}")

func(1, 2, 3, 4, x=10, y=20)
# a=1, b=2, args=(3, 4), kwargs={'x': 10, 'y': 20}
```

### 常见错误
```python
# 重复关键字参数
# func(a=1, **{"a": 2})  # TypeError: multiple values for 'a'
```

### 实际应用
```python
def create_config(**settings):
    default_config = {
        "theme": "dark", "font_size": 14,
        "auto_save": True, "language": "zh-CN"
    }
    default_config.update(settings)
    return default_config

config = create_config(theme="light", font_size=18)
print(config)
```

### 动手练习
```python
# 实现一个函数，接收任意关键字参数，只返回值为字符串的键值对
def filter_strings(**kwargs):
    # TODO
    pass

print(filter_strings(a="hello", b=42, c="world", d=True))
# {'a': 'hello', 'c': 'world'}
```

---

## 7. 仅位置参数(/)和仅关键字参数(*)

### 说明
Python 3.8+ 新增。用 `/` 标记前面的参数只能位置传递，用 `*` 标记后面的参数只能关键字传递。

### 语法
```python
def 函数名(仅位置参数, /, 普通参数, *, 仅关键字参数):
    函数体
```

### 示例
```python
# / 前面的参数只能按位置传
def func_pos(a, b, /, c, d):
    print(a, b, c, d)

func_pos(1, 2, 3, d=4)     # 正确：1 2 3 4
# func_pos(a=1, b=2, c=3, d=4)  # TypeError

# * 后面的参数只能按关键字传
def func_kw(a, b, *, c, d):
    print(a, b, c, d)

func_kw(1, 2, c=3, d=4)    # 正确
# func_kw(1, 2, 3, 4)     # TypeError

# 组合使用
def func_all(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)

func_all(1, 2, 3, d=4, e=5, f=6)  # 1 2 3 4 5 6
```

### 实际应用
```python
def divide(numerator, denominator, /, *, precision=2):
    """分子分母必须位置传，精度可以关键字传"""
    return round(numerator / denominator, precision)

print(divide(10, 3, precision=4))  # 3.3333
print(divide(10, 3))               # 3.33
```

---

## 8. 参数解包

### 说明
用 `*` 解包列表/元组作为位置参数，用 `**` 解包字典作为关键字参数。

### 示例
```python
def add(a, b, c):
    return a + b + c

# * 解包列表
args = [1, 2, 3]
print(add(*args))  # 6

# ** 解包字典
kwargs = {"a": 10, "b": 20, "c": 30}
print(add(**kwargs))  # 60

# 合并两个字典（Python 3.5+）
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = {**dict1, **dict2}
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

### 实际应用
```python
def wrapper(*args, **kwargs):
    print(f"调用参数: args={args}, kwargs={kwargs}")
    return real_function(*args, **kwargs)

def real_function(a, b, c):
    return a + b + c

print(wrapper(1, 2, c=3))
```

---

## 9. 参数优先级顺序

### 说明
完整参数定义顺序：仅位置参数(/前) → 普通参数 → *args → 仅关键字参数(*后) → **kwargs

### 示例
```python
def full_signature(pos_only, /, normal, *args, kw_only, **kwargs):
    print(f"pos_only={pos_only}, normal={normal}, args={args}, kw_only={kw_only}, kwargs={kwargs}")

full_signature(1, 2, 3, 4, kw_only=5, extra=6)
# pos_only=1, normal=2, args=(3, 4), kw_only=5, kwargs={'extra': 6}
```

---

## 总结

| 参数类型 | 语法 | 调用方式 |
|----------|------|----------|
| 位置参数 | `def f(a, b)` | `f(1, 2)` |
| 关键字参数 | `def f(a, b)` | `f(a=1, b=2)` |
| 默认参数 | `def f(a=1)` | `f()` 或 `f(2)` |
| *args | `def f(*args)` | `f(1, 2, 3)` |
| **kwargs | `def f(**kw)` | `f(a=1, b=2)` |
| 仅位置参数 | `def f(a, /)` | `f(1)` |
| 仅关键字参数 | `def f(*, a)` | `f(a=1)` |
