# Day 1：挑战顺序

> 每题只增加一个新动作。卡住时先运行题目底部的测试，再只改一个函数。

## 挑战 1：函数输入、return 与字典增改（★☆☆☆☆）

写 `create_person(name, age)`，返回：

```python
{"姓名": name, "年龄": age}
```

## 挑战 2：简单配置覆盖（★★☆☆☆）

写 `merge_config(default, override)`。

规则：后面字典的同名键覆盖前面字典；新键直接添加。不处理嵌套字典。

## 挑战 3：默认设置函数（★★★☆☆）

写 `create_report_settings()`，使用默认参数返回设置字典。

## 挑战 4：函数选择器（★★★★☆）

把加、减、乘、除函数放进字典；根据 `action` 选择一个函数执行。

## 挑战 5：逐行打印报告（★★★☆☆）

文件：`starter/challenge05.py`

```python
print_report("数学成绩", ["小明", "小红"], [90, 85])
```

输出：

```text
数学成绩
小明：90分
小红：85分
```

只用普通参数、列表、`for`、`range`、`print`。

## 终极挑战：个人信息报告（★★★★☆）

文件：`starter/ultimate.py`

- `build_person_report(name, age, city, hobbies)` 返回字典；
- `show_person_report(person)` 逐行打印字典；
- 不使用 `*args`、`**kwargs`、类、闭包、递归。

终极挑战没有新知识，只是组合前面做过的动作。
