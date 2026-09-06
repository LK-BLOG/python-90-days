# Day 3：字符串与文本处理

## 今天要做出的东西

一个**文本信息分析器**：输入一段文字，输出清洗后的文本、单词数量、关键词和摘要。

今天不再讲函数参数。函数只作为工具使用，重点放在字符串本身。

## 前置

- Day 1：会写函数和 return；
- Day 2：会用列表、字典和 for 循环。

## 今天学什么

- 字符串索引和切片；
- `lower()`、`upper()`、`strip()`；
- `split()`：字符串拆成列表；
- `join()`：列表拼成字符串；
- `replace()`：替换文本；
- f-string 输出；
- 多行文本处理；
- 用多个小函数完成文本分析。

## 执行顺序

1. 运行 `examples/` 中的字符串示例；
2. 完成 `starter/challenge01.py`：切片和清洗；
3. 完成 `starter/challenge02.py`：拆分单词；
4. 完成 `starter/challenge03.py`：替换敏感词；
5. 完成 `starter/challenge04.py`：统计文本；
6. 完成 `starter/challenge05.py`：文本分析器；
7. 完成 `starter/ultimate.py`：日志摘要工具；
8. 把完成版放入 `code/`。

## 最小示例

```python
text = "  Hello Python, Python is useful.  "

text = text.strip()
text = text.lower()
words = text.replace(",", "").replace(".", "").split()

print(words)
print(" ".join(words))
```

## 完成标准

- [ ] 会用切片取出字符串的一部分；
- [ ] 会用 `strip()` 清理两端空白；
- [ ] 会用 `split()` 得到列表；
- [ ] 会用 `join()` 拼接列表；
- [ ] 会用 `replace()` 替换内容；
- [ ] 能统计字数、行数和关键词；
- [ ] 能把多个字符串函数拆开组合。
