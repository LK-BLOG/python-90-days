# 挑战五(Boss)：函数式数据管道

## 难度
★★★★★

## 目标
用函数参数系统构建一个灵活的数据处理管道。

## 背景
数据处理是Python最常见的用途之一。你需要用纯函数和参数组合，构建一个可复用的数据管道系统。

## 功能要求

### 核心函数
```python
def pipeline(data, *operations, **config)
```
接收数据和多个处理操作，按顺序执行并返回结果。

### 操作函数
```python
def op_filter(data, condition=None, key=None)
def op_map(data, func=None, key=None)
def op_sort(data, key=None, reverse=False)
def op_group(data, key=None, agg=None)
def op_limit(data, n=10)
def op_unique(data, key=None)
```

### 参数设计
- 每个操作函数必须使用 *args 和 **kwargs 灵活接收参数
- 支持链式调用：pipeline(data).filter(...).map(...).sort(...).result()
- 操作可组合、可复用

## 示例
```python
students = [
    {"name": "Alice", "age": 20, "score": 85},
    {"name": "Bob", "age": 22, "score": 92},
    {"name": "Charlie", "age": 20, "score": 78},
]

result = pipeline(students,
    op_filter(key="age", condition=lambda x: x >= 20),
    op_sort(key="score", reverse=True),
    op_limit(n=2),
)
# [{"name": "Bob", ...}, {"name": "Alice", ...}]
```

## 验收标准
1. ✅ pipeline 函数支持 *args 和 **kwargs
2. ✅ 所有操作函数参数设计灵活
3. ✅ 链式调用接口可用
4. ✅ 支持嵌套数据操作
5. ✅ 有完整的使用示例和测试
