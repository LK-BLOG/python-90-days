# Day 5: Boss挑战 — CSV数据分析器

## 目标
用collections模块分析CSV数据。

## 功能要求
```python
def analyze_csv(data, group_by=None, sort_by=None, agg_func=None):
    """分析CSV数据"""
    # group_by: 分组字段
    # sort_by: 排序字段
    # agg_func: 聚合函数(sum/avg/count/min/max)
```

## 示例
```python
data = [
    {"name": "张三", "dept": "技术", "salary": 10000},
    {"name": "李四", "dept": "销售", "salary": 8000},
    {"name": "王五", "dept": "技术", "salary": 12000},
]
result = analyze_csv(data, group_by="dept", agg_func="avg")
# {"技术": 11000, "销售": 8000}
```
