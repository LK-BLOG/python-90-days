# Day 1: Boss挑战 — 多格式报告生成器

## 项目名称
**Multi-Format Report Generator**

## 目标
用函数参数的灵活组合，构建一个支持多种输出格式的报告生成器。

## 背景
同一份数据经常需要以不同格式展示：纯文本表格、CSV、Markdown表格等。
你需要设计一个参数灵活的函数接口，让调用者能用各种方式传入配置。

## 功能要求

### 核心函数 `generate_report()`
```python
def generate_report(title, headers, rows, format="text", separator=",", 
                    show_total=False, sort_by=None, max_width=None):
    """
    生成格式化报告
    - title: 报告标题（必填，仅位置参数）
    - headers: 列名列表
    - rows: 数据行（二维列表）
    - format: 输出格式 "text"/"csv"/"markdown"/"html"
    - separator: CSV分隔符
    - show_total: 是否显示数字列统计
    - sort_by: 按第几列排序
    - max_width: text格式最大列宽
    """
```

### 四种输出格式
1. **text** — 纯文本对齐表格（带边框）
2. **csv** — CSV格式（可指定分隔符）
3. **markdown** — Markdown表格
4. **html** — HTML `<table>` 标签

### 辅助函数（练习 *args 和 **kwargs）
```python
def print_report(*columns, **options):
    """打印报告的便捷接口，*columns 接收列数据，**options 接收格式选项"""
    pass

def compare_reports(*reports, show_diff=False):
    """接收多份报告字符串，输出对比"""
    pass
```

## 示例
```python
headers = ["Name", "Age", "Score"]
rows = [
    ["Alice", 20, 85],
    ["Bob", 22, 92],
    ["Charlie", 20, 78],
]

# 默认文本表格
print(generate_report("Class Report", headers, rows))

# CSV格式
print(generate_report("Class Report", headers, rows, format="csv"))

# 带排序和统计
print(generate_report("Class Report", headers, rows, 
                       format="markdown", sort_by=2, show_total=True))

# 用 **kwargs 解包传参
options = {"format": "csv", "separator": ";", "sort_by": 2}
print(generate_report("Class Report", headers, rows, **options))
```

## 验收标准
1. ✅ 四种格式全部正确输出
2. ✅ sort_by 排序正确
3. ✅ show_total 正确计算数字列统计
4. ✅ *args 和 **kwargs 用法正确
5. ✅ 参数设计合理，调用方式灵活

## 可选扩展
- 支持条件过滤行
- 支持自定义颜色标记（ANSI）
- 支持合并单元格
