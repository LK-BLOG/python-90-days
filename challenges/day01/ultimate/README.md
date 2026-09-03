# 挑战五(Boss)：多格式报告生成器

## 难度
★★★★★

## 目标
用函数参数系统构建一个灵活的报告生成器，支持多种输出格式。

## 背景
同一份数据需要以不同格式输出（纯文本表格、CSV、Markdown表格等）。
你需要设计一个参数灵活的函数接口，让调用者能用各种方式传入配置。

## 你已经会的知识
- 位置参数、关键字参数、默认参数
- *args 接收任意数量位置参数
- **kwargs 接收任意关键字参数
- 参数解包
- 基本的字符串操作（拼接、格式化）

## 功能要求

### 核心函数
```python
def generate_report(title, headers, rows, format="text", separator=",", 
                    show_total=False, sort_by=None, max_width=None):
    """
    生成格式化报告
    
    Args:
        title: 报告标题
        headers: 列名列表
        rows: 数据行（二维列表）
        format: 输出格式 ("text", "csv", "markdown", "html")
        separator: CSV分隔符
        show_total: 是否显示统计行
        sort_by: 按第几列排序（列编号，从0开始）
        max_width: 文本格式的最大列宽
    
    Returns:
        格式化的报告字符串
    """
```

### 四种输出格式
1. **text** — 纯文本对齐表格
   ```
   +----------+-----+-------+
   | Name     | Age | Score |
   +----------+-----+-------+
   | Alice    |  20 |    85 |
   | Bob      |  22 |    92 |
   +----------+-----+-------+
   ```

2. **csv** — CSV格式（可指定分隔符）
   ```
   Name,Age,Score
   Alice,20,85
   Bob,22,92
   ```

3. **markdown** — Markdown表格
   ```
   | Name | Age | Score |
   |------|-----|-------|
   | Alice| 20  | 85    |
   | Bob  | 22  | 92    |
   ```

4. **html** — HTML表格

### 辅助函数（练习 *args 和 **kwargs）
```python
def print_report(*columns, **options):
    """打印报告的便捷接口"""
    # *columns: 列数据
    # **options: 所有格式选项
    pass

def compare_reports(*reports, show_diff=False):
    """对比多份报告"""
    # 接收多份报告，输出对比
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

# 基础用法
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
2. ✅ sort_by 排序正确（数字列和文字列都能排）
3. ✅ show_total 正确计算数字列的统计
4. ✅ *args 和 **kwargs 用法正确
5. ✅ 参数设计合理，调用方式灵活

## 可选扩展
- 支持合并单元格（text/html）
- 支持按条件过滤行
- 支持自定义颜色标记（ANSI）
