# Day 6: Boss挑战 — 健壮的数据加载器

## 目标
从多种格式加载数据，完整错误处理。

## 功能要求
```python
def load_data(source, format=None):
    """从多种来源加载数据"""
    # 支持: JSON, CSV, TXT, dict
    # 完整错误处理
    # 自动检测格式
```

## 示例
```python
data = load_data("data.json")           # 自动检测JSON
data = load_data("data.csv", format="csv")
data = load_data({"key": "value"})      # 直接返回dict
```
