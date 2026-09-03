# Day 4: 字符串高级 — 完整教学

---

## 1. 字符串切片

### 说明
切片语法：`string[start:end:step]`，支持正向和反向索引。

### 示例
```python
s = "Hello, Python!"
print(s[0:5])     # Hello
print(s[7:13])    # Python
print(s[-7:-1])   # Python
print(s[::-1])    # !nohtyP ,olleH（反转）
print(s[::2])     # Hlo yhn（步长2）
print(s[1::2])    # el oPt（从index1开始）
```

### 常见错误
```python
s = "Hello"
s[0] = "h"  # TypeError: 字符串不可变！
# 解决：创建新字符串
s = "h" + s[1:]  # "hello"
```

---

## 2. split / join / replace

### 示例
```python
# split
csv_line = "张三,25,北京,工程师"
parts = csv_line.split(",")  # ['张三', '25', '北京', '工程师']

# 多分隔符
import re
text = "hello world;python,java"
parts = re.split(r'[;,\s]+', text)

# join
words = ["Hello", "World"]
sentence = " ".join(words)     # "Hello World"
csv_data = ",".join(words)     # "Hello,World"

# replace
text = "Hello World Hello Python"
new_text = text.replace("Hello", "Hi")         # "Hi World Hi Python"
new_text = text.replace("Hello", "Hi", 1)       # "Hi World Hello Python"
```

---

## 3. f-string 高级用法

### 示例
```python
name = "张三"
age = 25
score = 85.678

# 基础
print(f"姓名: {name}, 年龄: {age}")

# 表达式
print(f"明年: {age + 1}")
print(f"{'成年' if age >= 18 else '未成年'}")

# 格式化
print(f"分数: {score:.2f}")      # 85.68
print(f"百分比: {0.856:.1%}")     # 85.6%
print(f"宽度: {name:>10}")        #         张三
print(f"零填充: {42:05d}")        # 00042
print(f"千分位: {1234567:,}")     # 1,234,567

# 调用方法
print(f"大写: {name.upper()}")
print(f"分割: {'hello-world'.replace('-', ' ')}")

# 格式化日期
from datetime import datetime
now = datetime.now()
print(f"日期: {now:%Y-%m-%d %H:%M}")
```

---

## 4. 字符串方法链

### 示例
```python
# 链式调用
result = "  Hello, World!  ".strip().lower().replace("world", "python")
print(result)  # "hello, python!"

# 实际应用：数据清洗
raw = "  Zhang_San@Email.COM  "
cleaned = raw.strip().lower().replace("_", " ").split("@")[0]
print(cleaned)  # "zhang san"
```

---

## 5. 正则表达式基础

### 说明
re模块提供正则表达式支持。常用函数：match, search, findall, sub

### 示例
```python
import re

text = "我的电话是13812345678，邮箱是test@example.com"

# re.match — 从字符串开头匹配
m = re.match(r'\d+', '123abc')
print(m.group())  # 123

m = re.match(r'\d+', 'abc123')
print(m)  # None — 不是从开头匹配的

# re.search — 搜索第一个匹配
m = re.search(r'\d{11}', text)
print(m.group())  # 13812345678

# re.findall — 找到所有匹配
numbers = re.findall(r'\d+', text)
print(numbers)  # ['13812345678']

# re.sub — 替换
censored = re.sub(r'\d{11}', '1**********', text)
print(censored)
```

### 分组捕获
```python
import re

# 基础分组
pattern = r'(\d{4})-(\d{2})-(\d{2})'
date = "今天是2024-01-15，天气不错"
m = re.search(pattern, date)
if m:
    print(m.group(0))  # 2024-01-15（整个匹配）
    print(m.group(1))  # 2024
    print(m.group(2))  # 01
    print(m.group(3))  # 15
    print(m.groups())  # ('2024', '01', '15')

# 命名分组
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
m = re.search(pattern, date)
if m:
    print(m.group('year'))   # 2024
    print(m.groupdict())    # {'year': '2024', 'month': '01', 'day': '15'}

# findall带分组返回元组列表
log = "2024-01-15 ERROR: 失败 2024-01-16 INFO: 成功"
entries = re.findall(r'(\d{4}-\d{2}-\d{2}) (ERROR|INFO)', log)
print(entries)  # [('2024-01-15', 'ERROR'), ('2024-01-16', 'INFO')]
```

### 常见错误
```python
import re
# 忘记转义特殊字符
# re.search(r'(hello)', text) — ()是分组，不是字面括号
re.search(r'\(hello\)', text)  # 正确转义

# 贪婪 vs 非贪婪
html = '<div>hello</div><div>world</div>'
print(re.findall(r'<div>.*</div>', html))     # 贪婪：整个字符串
print(re.findall(r'<div>.*?</div>', html))     # 非贪婪：两个div
```

---

## 总结

| 技术 | 用途 |
|------|------|
| 切片 | 截取/反转字符串 |
| split/join | 分割和拼接 |
| f-string | 格式化输出 |
| re.match | 开头匹配 |
| re.search | 搜索匹配 |
| re.findall | 全部匹配 |
| re.sub | 替换匹配 |
| 分组捕获 | 提取子串 |
