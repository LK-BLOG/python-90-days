# Day 2：列表处理与函数拆分

## 1. 列表是可修改的数据集合

列表可以保存多个值，也可以在程序运行时增加、删除和修改。

```python
items = ["药水", "木剑"]
items.append("盾牌")
items[0] = "超级药水"
print(items)
```

### 常见错误

```python
items = ["药水"]
items[1] = "木剑"  # 错误：下标1还不存在
```

新增元素使用 `append()`，不要用不存在的下标赋值。

### 动手练习

创建一个 `skills` 列表，添加三个技能，再把第二个技能改名。

## 2. `for` 遍历与下标

只需要值时：

```python
for item in items:
    print(item)
```

需要下标时：

```python
for index in range(len(items)):
    print(index, items[index])
```

今天先使用这种方式，不提前使用 `enumerate()`。

### 动手练习

写 `show_numbered_items(items)`，输出：

```text
1. 药水
2. 木剑
```

## 3. 添加、删除和查找

```python
def add_item(items, item):
    items.append(item)
    return items


def remove_item(items, item):
    if item in items:
        items.remove(item)
    return items


def contains_item(items, item):
    return item in items
```

### 实际应用

购物车、游戏背包、播放列表、任务列表都离不开这些操作。

### 动手练习

增加 `remove_all(items, item)`，一次删除所有同名元素。

## 4. 返回新列表

```python
def get_long_names(names, minimum_length):
    result = []

    for name in names:
        if len(name) >= minimum_length:
            result.append(name)

    return result
```

不要忘记 `return result`。没有 return，函数返回的是 `None`。

### 常见错误

```python
def get_long_names(names, minimum_length):
    result = []
    for name in names:
        if len(name) >= minimum_length:
            result.append(name)
    # 少了 return
```

### 动手练习

写 `get_expensive_items(items, limit)`，返回价格大于等于 limit 的物品。

## 5. 列表中的字典

```python
players = [
    {"name": "小明", "score": 80},
    {"name": "小红", "score": 95},
]

for player in players:
    print(player["name"], player["score"])
```

访问顺序是：先从列表取出一个字典，再用键取字典的值。

```python
player["score"]
```

### 动手练习

写函数返回所有分数大于等于80的玩家姓名。

## 6. 函数拆分

一个背包功能可以拆成：

```python
def add_item(items, item):
    """添加一个物品。"""
    pass


def find_item(items, name):
    """按名称查找物品。"""
    pass


def total_count(items):
    """统计所有物品数量。"""
    pass
```

拆分标准：

- 函数名说清楚动作；
- 一个函数只完成一个动作；
- 参数尽量少；
- 返回值明确；
- 错误由函数自己处理或明确抛出。

## 7. 今日项目骨架

```python
def add_item(items, name, kind, price, count=1):
    """向背包添加物品。"""
    item = {
        "name": name,
        "kind": kind,
        "price": price,
        "count": count,
    }
    items.append(item)
    return items


def find_item(items, name):
    """返回第一个同名物品，找不到返回 None。"""
    for item in items:
        if item["name"] == name:
            return item
    return None


def total_value(items):
    """计算背包总价值。"""
    total = 0
    for item in items:
        total += item["price"] * item["count"]
    return total
```

这只是示范接口，不是今天项目的完整答案。你需要自己补充删除、筛选、统计和打印。

## 8. 今天怎么调试

每写完一个函数，立刻单独测试：

```python
bag = []
add_item(bag, "药水", "消耗品", 30, 2)
print(bag)
print(find_item(bag, "药水"))
print(total_value(bag))
```

不要等所有功能写完才第一次运行。

## 今日任务顺序

1. 完成列表基础练习；
2. 写 `add_item`；
3. 写 `remove_item`；
4. 写 `find_item`；
5. 写统计函数；
6. 组合成背包程序；
7. 增加空列表和不存在物品测试；
8. 把最终版本放入 `code/`。
