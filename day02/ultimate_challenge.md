# Day 2: Boss挑战 — 数据管道处理系统

## 目标
用函数组合构建灵活的数据处理管道。

## 功能要求

### 核心函数
```python
def pipeline(data, *transforms)  # 依次应用转换
def compose(*funcs)              # 组合函数
def pipe(data)                   # 链式调用
```

### 转换函数
remove_none, flatten, unique, sort_by, group_by, filter_by, map_values, chunk

## 示例
```python
raw = [3, None, 1, None, 4, 1, 5]
cleaned = pipeline(raw, remove_none, unique, sorted)
print(cleaned)  # [1, 3, 4, 5]
```

## 验收标准
1. ✅ pipeline正常工作
2. ✅ compose组合正确
3. ✅ 链式调用正常
4. ✅ 所有转换函数正确
