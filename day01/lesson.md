# Day 1 课程：函数参数

## 学习目标

今天不追求“知道很多”，只追求一件事：**能设计灵活的函数接口**。

最终你要写出：

```python
def generate_report(title, headers, rows, format="text", **options):
    ...
```

## 1. 位置参数与关键字参数

### 作用

让函数接收调用者传入的数据。

### 语法

```python
def 函数名(参数1, 参数2):
    函数体
```

### 示例

```python
def create_user(name, age):
    return {"name": name, "age": age}

print(create_user("Alice", 20))
print(create_user(name="Bob", age=22))
```

### 常见错误

```python
# 错误：给同一个参数传了两次
create_user("Alice", name="Bob", age=20)
```

### 实际应用

API函数、配置函数、业务服务函数都需要清晰的参数接口。

### 动手练习

把 `create_user` 增加一个 `email` 参数，并分别用位置参数和关键字参数调用。

## 2. 默认参数

### 作用

让调用者可以省略常用配置。

### 语法

```python
def connect(host, port=80):
    ...
```

### 示例

```python
def format_price(price, currency="CNY"):
    return f"{price:.2f} {currency}"

print(format_price(99))
print(format_price(99, "USD"))
```

### 常见错误：可变默认参数

不要这样写：

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

正确写法：

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 实际应用

默认分页数量、默认输出格式、默认超时时间。

### 动手练习

给报告函数增加默认格式、默认分隔符和默认排序方式。

## 3. `*args`：收集任意位置参数

### 作用

当参数数量不确定时使用。

### 语法

```python
def function(first, *args):
    ...
```

`args` 是元组：

```python
def inspect_args(*args):
    print(type(args))
    print(args)

inspect_args("a", "b", "c")
```

### 常见错误

```python
# 错误：把 args 当成单个值
# args 是 tuple，需要遍历或按索引访问
```

### 实际应用

日志函数、批量处理函数、事件触发函数。

### 动手练习

写一个 `join_words(*words, separator=" ")`，把任意数量的单词拼接起来。

## 4. `**kwargs`：收集任意关键字参数

### 作用

接收不固定名称的配置项。

### 语法

```python
def function(**kwargs):
    ...
```

`kwargs` 是字典：

```python
def print_options(**options):
    for key, value in options.items():
        print(f"{key} = {value}")

print_options(color="blue", size=12)
```

### 常见错误

```python
# 错误：忘记调用 items()
# kwargs.items() 才能同时遍历键和值
```

### 实际应用

配置系统、HTTP请求选项、插件参数。

### 动手练习

写一个 `build_url(base, **params)`，把关键字参数拼成查询字符串。

## 5. 参数解包

### 列表解包

```python
def add(a, b, c):
    return a + b + c

values = [1, 2, 3]
print(add(*values))
```

### 字典解包

```python
def create_user(name, age):
    return {"name": name, "age": age}

user = {"name": "Alice", "age": 20}
print(create_user(**user))
```

### 动手练习

把一个报告配置字典解包传给 `generate_report`。

## 6. 位置专用参数和关键字专用参数

### 语法

```python
def example(positional_only, /, normal, *, keyword_only):
    ...
```

- `/` 前面只能按位置传递；
- `*` 后面只能按关键字传递。

### 示例

```python
def open_report(path, /, *, encoding="utf-8"):
    return f"打开 {path}，编码 {encoding}"

open_report("report.txt", encoding="utf-8")
```

### 动手练习

把报告标题设计成仅位置参数，把输出格式设计成仅关键字参数。

## 7. 综合：设计函数接口

```python
def generate_report(title, headers, rows, format="text", **options):
    """生成报告的函数接口。"""
    print(f"标题: {title}")
    print(f"列: {headers}")
    print(f"行数: {len(rows)}")
    print(f"格式: {format}")
    print(f"额外选项: {options}")


generate_report(
    "成绩报告",
    ["姓名", "分数"],
    [["Alice", 90]],
    format="markdown",
    show_total=True,
)
```

这段代码先不要求你实现格式化，只要求你看懂参数如何进入函数。

## 今日实践顺序

1. 运行 `examples/` 中的示例；
2. 完成 `starter/01_basics_practice.py`；
3. 完成 `starter/02_args_practice.py`；
4. 完成 `starter/challenge01.py` 到 `challenge05.py`；
5. 完成 `starter/ultimate.py`；
6. 把最终版本复制到 `code/`。

## 今日验收

```bash
python -m unittest discover -s tests
```

如果测试失败，先看错误信息，再回到对应函数修改。不要直接跳到下一天。
