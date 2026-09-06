# Day 3：字符串与文本处理

## 1. 字符串索引和切片

字符串可以通过下标读取单个字符，也可以切出一段。

```python
text = "Python"
print(text[0])
print(text[-1])
print(text[0:3])
print(text[::2])
```

字符串不能直接修改：

```python
# text[0] = "J"  # 错误
text = "J" + text[1:]
```

动手练习：取出一段身份证号的前六位和后四位。

## 2. 清理字符串

```python
text = "  Hello Python  "
print(text.strip())
print(text.lower())
print(text.upper())
```

实际文本经常有多余空格、大小写不一致和换行，需要先清理再分析。

## 3. `split()`：拆分

```python
text = "Python,Java,Go"
languages = text.split(",")
print(languages)
```

按空白拆分：

```python
sentence = "Python is easy to learn"
words = sentence.split()
print(words)
```

## 4. `join()`：拼接

```python
words = ["Python", "is", "useful"]
sentence = " ".join(words)
print(sentence)
```

`join()` 的左边是分隔符，括号里必须是一组字符串。

```python
# ",".join(["a", 2])  # 错误：2不是字符串
",".join(["a", str(2)])
```

## 5. `replace()`：替换

```python
text = "我喜欢Java"
text = text.replace("Java", "Python")
print(text)
```

可以连续替换：

```python
text = "  Hello, Python!  "
cleaned = text.strip().replace(",", "").replace("!", "")
print(cleaned)
```

## 6. 多行文本

```python
log = """INFO start
ERROR failed
INFO retry"""

lines = log.splitlines()
for line in lines:
    print(line)
```

`splitlines()` 比 `split("\n")` 更适合处理不同平台的换行。

## 7. 字符串统计

```python
def count_words(text):
    words = text.strip().split()
    return len(words)

print(count_words("Python makes text processing easy"))
```

统计关键词：

```python
def count_keyword(text, keyword):
    return text.lower().count(keyword.lower())
```

## 8. 文本分析器设计

把大问题拆成小函数：

```python
def clean_text(text):
    return text.strip().lower()


def get_lines(text):
    return text.splitlines()


def get_words(text):
    return text.split()


def build_summary(text):
    return {
        "字符数": len(text),
        "行数": len(get_lines(text)),
        "单词数": len(get_words(text)),
    }
```

今天的终极项目就是把这些动作组合起来。

## 常见错误

### 忘记字符串不可变

```python
text.replace("old", "new")
# 没有保存返回值，text本身不会改变
```

正确：

```python
text = text.replace("old", "new")
```

### `join()` 拼数字

先用 `str()` 转成字符串。

### 空字符串

```python
"".split()  # []
"".strip()  # ""
```

必须考虑输入为空的情况。

## 今日项目：日志摘要工具

输入：

```text
INFO user login
ERROR database timeout
INFO retry success
```

输出：

```text
总行数：3
INFO：2
ERROR：1
错误摘要：database timeout
```

要求：

- 清理每一行；
- 按空格拆分；
- 判断日志级别；
- 用字典统计数量；
- 返回报告字符串。

## 调试顺序

```python
sample = "INFO start\nERROR failed"
print(sample.splitlines())
print(clean_text(sample))
print(build_summary(sample))
```

每完成一个函数就运行一次，不要全部写完才调试。
