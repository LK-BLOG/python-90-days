# Day 2：列表处理与函数拆分

## 今天要做出的东西

一个**游戏背包处理器**：能添加物品、删除物品、查找物品、统计数量和计算总价值。

今天不学 `lambda`、`map`、`filter`、闭包或高阶函数。它们放到后面，别提前混进来。

## 学习顺序

1. 运行 `examples/`，观察列表怎么被函数处理；
2. 完成 `starter/01_list_practice.py`；
3. 完成 `starter/02_inventory_practice.py`；
4. 依次完成 `starter/challenge01.py` 到 `challenge05.py`；
5. 完成 `starter/ultimate.py`；
6. 最终版本复制到 `code/`。

## 今天的核心知识

### 1. 遍历列表

```python
items = ["药水", "木剑", "盾牌"]

for item in items:
    print(item)
```

### 2. `append()` 添加

```python
items = []
items.append("药水")
items.append("木剑")
print(items)
```

### 3. `remove()` 删除

```python
items = ["药水", "木剑"]
items.remove("药水")
print(items)
```

如果元素不存在会报错，所以实际代码要先判断：

```python
if "药水" in items:
    items.remove("药水")
```

### 4. 通过下标修改

```python
scores = [80, 90, 70]
scores[1] = 95
print(scores)
```

### 5. 函数返回新列表

```python
def double_numbers(numbers):
    result = []

    for number in numbers:
        result.append(number * 2)

    return result
```

注意：`result` 是函数内部的新列表，不要直接改掉调用者传进来的列表，除非题目明确要求。

### 6. 用 `len()`、`sum()` 做统计

```python
scores = [80, 90, 70]
print(len(scores))
print(sum(scores))
```

### 7. 把大问题拆成小函数

不要写一个几百行的函数：

```python
def run_inventory():
    # 添加
    # 删除
    # 查找
    # 统计
    # 打印
    pass
```

拆成：

```python
def add_item(items, item):
    ...

def remove_item(items, item):
    ...

def find_item(items, keyword):
    ...

def count_items(items):
    ...
```

每个函数只做一件事，出错时更容易定位。

## 今天的项目：游戏背包

数据先使用简单字典列表：

```python
items = [
    {"name": "治疗药水", "kind": "消耗品", "price": 30, "count": 2},
    {"name": "木剑", "kind": "武器", "price": 50, "count": 1},
]
```

你要逐步实现：

```text
添加物品
删除物品
按名称查找
按类型筛选
统计物品总数
计算背包总价值
打印背包
```

## 今天的加餐

必修完成后再做：

- 处理空列表；
- 处理删除不存在的物品；
- 处理数量为0或负数；
- 给物品增加重量字段，计算背包总重量；
- 让同名物品自动叠加数量；
- 把背包拆成多个函数文件。

## 完成标准

- [ ] 能遍历列表；
- [ ] 会用 `append()` 添加元素；
- [ ] 会用 `remove()` 删除元素；
- [ ] 会通过下标修改元素；
- [ ] 能让函数返回新列表；
- [ ] 能把一个项目拆成多个函数；
- [ ] 能完成背包项目的添加、删除、查找、统计。
