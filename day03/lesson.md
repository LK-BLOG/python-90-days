# Day 3：函数参数设计

今天的主题不是“记住几种写法”，而是学会设计一个别人容易调用的函数。

## 1. 位置参数

### 知识点

函数定义中的参数，调用时按照位置对应。

```python
def create_user(name, age):
    return {"name": name, "age": age}

user = create_user("小戡", 9)
print(user)
```

第一个值给 `name`，第二个值给 `age`。

### 常见错误

```python
create_user("小戡")
# TypeError：少了 age
```

```python
create_user("小戡", 9, "北京")
# TypeError：多了参数
```

### 动手练习

写 `create_item(name, price, count)`，返回包含三个字段的字典。

## 2. 关键字参数

### 知识点

调用时写出参数名，顺序可以改变。

```python
def create_user(name, age, city):
    return {"name": name, "age": age, "city": city}

user = create_user(age=9, city="北京", name="小戡")
print(user)
```

### 位置参数和关键字参数混用

位置参数必须放在关键字参数前面：

```python
create_user("小戡", age=9, city="北京")
```

错误写法：

```python
# create_user(name="小戡", 9, city="北京")
```

### 动手练习

把 Day 2 的 `add_item` 分别用位置方式和关键字方式调用。

## 3. 默认参数

### 知识点

默认参数允许调用者省略常用配置。

```python
def create_report(title, format="text", separator="|"):
    return {
        "title": title,
        "format": format,
        "separator": separator,
    }

print(create_report("成绩报告"))
print(create_report("成绩报告", format="csv"))
```

### 参数定义顺序

没有默认值的参数必须放在有默认值的参数前面：

```python
# 正确
# def report(title, format="text"):
#     pass

# 错误
# def report(format="text", title):
#     pass
```

### 动手练习

给报告设置增加 `show_total=False` 和 `encoding="utf-8"`。

## 4. 可变默认参数陷阱

### 错误写法

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("python"))
print(add_tag("ai"))
```

第二次调用可能得到：

```python
["python", "ai"]
```

因为这个列表只在函数定义时创建一次，后续调用会继续使用它。

### 正确写法

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []

    tags.append(tag)
    return tags
```

### 动手练习

修复一个使用 `items=[]` 的购物车函数。

## 5. 参数校验

参数设计不只是“接收值”，还要拒绝明显错误。

```python
def create_score(name, score):
    if score < 0 or score > 100:
        raise ValueError("分数必须在 0 到 100 之间")

    return {"name": name, "score": score}
```

### 动手练习

给 `create_report` 增加检查：标题不能为空，格式只能是 `text` 或 `csv`。

## 6. 参数解包预览

这一节只看懂，不作为今天的主要任务。

列表可以用 `*` 拆开：

```python
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))
```

字典可以用 `**` 拆开：

```python
def create_user(name, age):
    return {"name": name, "age": age}

user = {"name": "小戡", "age": 9}
print(create_user(**user))
```

Day 4 再正式学习 `*args` 和 `**kwargs`。

## 7. 今日小项目：成绩单设置生成器

目标接口：

```python
def make_settings(
    title="未命名报告",
    format="text",
    separator="|",
    show_total=False,
):
    ...
```

要求：

- 返回一个字典；
- 默认调用能正常工作；
- 关键字参数可以覆盖默认设置；
- 非法格式抛出 `ValueError`；
- 不修改外部传入的列表或字典。

## 调试顺序

每写一个函数就立即测试：

```python
print(make_settings())
print(make_settings(title="数学成绩", format="csv"))
```

再测试错误：

```python
# print(make_settings(format="xml"))
```

## 今日任务

1. 完成位置参数练习；
2. 完成关键字参数练习；
3. 完成默认参数练习；
4. 修复可变默认参数；
5. 加入参数校验；
6. 完成成绩单设置生成器。
