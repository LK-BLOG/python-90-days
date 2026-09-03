# Day 6: 异常处理 — 完整教学

---

## 1. try/except/else/finally

### 说明
完整的异常处理链：try（尝试）→ except（捕获）→ else（无异常时执行）→ finally（始终执行）

### 示例
```python
# 基础
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除以零！")

# 捕获多个异常
try:
    value = int(input("输入数字: "))
    result = 100 / value
except ValueError:
    print("不是数字！")
except ZeroDivisionError:
    print("不能除以零！")

# 捕获所有异常（谨慎使用）
try:
    risky_code()
except Exception as e:
    print(f"出错了: {type(e).__name__}: {e}")

# else — 没有异常时执行
try:
    data = open("config.txt").read()
except FileNotFoundError:
    data = "default config"
else:
    print("文件读取成功")
finally:
    print("这段始终执行")
```

### 常见错误
```python
# 过于宽泛的异常捕获
try:
    risky_code()
except:  # 不推荐！连 KeyboardInterrupt 都捕获了
    pass

# 吞掉异常
try:
    risky_code()
except Exception:
    pass  # 异常被静默忽略，debug时很痛苦

# 正确做法：至少记录日志
import logging
try:
    risky_code()
except Exception as e:
    logging.error(f"出错了: {e}")
    raise  # 重新抛出
```

---

## 2. 异常层级

### 说明
所有异常继承自 BaseException，常用的是 Exception 的子类。

### 常见异常层级
```python
BaseException
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ValueError
      ├── TypeError
      ├── KeyError
      ├── IndexError
      ├── FileNotFoundError
      ├── AttributeError
      ├── ZeroDivisionError
      └── RuntimeError
```

### 示例
```python
# 用 isinstance 做精确判断
try:
    x = int("abc")
except (ValueError, TypeError) as e:
    print(f"类型错误: {e}")

# 捕获特定层级
try:
    data = {"key": "value"}
    print(data["missing"])
except LookupError as e:  # KeyError是LookupError的子类
    print(f"查找失败: {e}")
```

---

## 3. raise — 主动抛出异常

### 示例
```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0 or age > 150:
        raise ValueError(f"年龄 {age} 不在合理范围内")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)  # 年龄 -5 不在合理范围内

# 重新抛出异常
try:
    risky_operation()
except Exception as e:
    log_error(e)  # 记录日志
    raise         # 重新抛出，让上层处理
```

---

## 4. 自定义异常类

### 示例
```python
class AppError(Exception):
    """应用基础异常"""
    pass

class ValidationError(AppError):
    """数据验证错误"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"字段 {field}: {message}")

class NotFoundError(AppError):
    """资源未找到"""
    def __init__(self, resource, resource_id):
        super().__init__(f"{resource} (id={resource_id}) 未找到")

# 使用
def create_user(name, age):
    if not name:
        raise ValidationError("name", "不能为空")
    if age < 0:
        raise ValidationError("age", "不能为负数")
    return {"name": name, "age": age}

try:
    create_user("", 25)
except ValidationError as e:
    print(f"验证失败: {e}")
    print(f"字段: {e.field}")
```

---

## 5. 上下文管理器

### 示例
```python
# with语句自动管理资源
with open("file.txt", "w") as f:
    f.write("hello")
# 文件自动关闭，即使发生异常

# 自定义上下文管理器
class DatabaseConnection:
    def __init__(self, url):
        self.url = url
    
    def __enter__(self):
        print(f"连接到 {self.url}")
        self.connection = "connected"
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"发生错误: {exc_val}")
        print("关闭连接")
        return False  # 不抑制异常

with DatabaseConnection("mysql://localhost") as db:
    print(db.connection)
```

### contextlib 简化
```python
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.time()
    yield  # 这里是with块的入口
    print(f"{label}: {time.time() - start:.2f}s")

with timer("处理"):
    import time
    time.sleep(1)
# 输出: 处理: 1.00s
```

---

## 6. 防御性编程

### 示例
```python
# LBYL (Look Before You Leap) — 先检查
def get_value(data, key, default=None):
    if key in data:
        return data[key]
    return default

# EAFP (Easier to Ask Forgiveness than Permission) — 先做再处理
def get_value_eafp(data, key, default=None):
    try:
        return data[key]
    except KeyError:
        return default

# Python推荐EAFP风格

# 安全的类型转换
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# 安全的属性访问
def safe_getattr(obj, attr, default=None):
    return getattr(obj, attr, default)
```

---

## 总结

| 概念 | 用途 |
|------|------|
| try/except | 捕获异常 |
| else | 无异常时执行 |
| finally | 始终执行（清理） |
| raise | 主动抛出 |
| 自定义异常 | 语义化错误 |
| 上下文管理器 | 资源管理 |
| EAFP | 先做再处理 |
