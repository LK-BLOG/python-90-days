# Day 3: 作用域与闭包 — 完整教学

---

## 1. LEGB作用域规则

### 说明
Python查找变量的顺序：Local → Enclosing → Global → Built-in

### 示例
```python
# Built-in: 内置作用域（print, len, range等）
# Global: 模块级别
x = "global"

def outer():
    # Enclosing: 外部函数作用域
    x = "enclosing"
    
    def inner():
        # Local: 当前函数作用域
        x = "local"
        print(x)  # local
    
    inner()
    print(x)  # enclosing

outer()
print(x)  # global
```

### 常见错误
```python
x = 10

def modify():
    x = 20  # 这是新创建的局部变量，不是修改全局的x
    print(x)  # 20

modify()
print(x)  # 10 — 全局的x没变

# 想在函数内修改全局变量？用global
def modify_global():
    global x
    x = 20

modify_global()
print(x)  # 20
```

---

## 2. global 和 nonlocal

### 说明
- `global`：声明变量来自全局作用域
- `nonlocal`：声明变量来自外层函数作用域（Python 3+）

### 示例
```python
# global 使用
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)  # 2

# nonlocal 使用
def outer():
    count = 0
    
    def inner():
        nonlocal count
        count += 1
        return count
    
    return inner

counter = outer()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

### 常见错误
```python
def outer():
    x = 10
    def inner():
        x += 1  # UnboundLocalError!
        # Python看到x += 1就认为x是局部变量，但还没定义就使用了
        # 解决：加 nonlocal x
    inner()

# nonlocal不能用于全局变量
def func():
    nonlocal x  # SyntaxError: no binding for nonlocal
```

---

## 3. 闭包原理

### 说明
闭包 = 内部函数 + 引用了外部函数的变量 + 外部函数已返回。

### 示例
```python
def make_multiplier(n):
    """工厂函数：生成乘以n的函数"""
    def multiplier(x):
        return x * n  # n来自外部函数，但外部函数已返回
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# 闭包保存了外部变量
print(double.__closure__[0].cell_contents)  # 2
print(triple.__closure__[0].cell_contents)  # 3
```

### 闭包 vs 类
```python
# 闭包版本
def make_counter(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

# 类版本
class Counter:
    def __init__(self, start=0):
        self.count = start
    def __call__(self):
        self.count += 1
        return self.count

# 两者行为相同，闭包更轻量，类更灵活
```

### 实际应用
```python
# 缓存（简单版）
def make_cached(func):
    cache = {}
    def cached(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return cached

@make_cached
def expensive_calc(n):
    print(f"计算 {n}...")
    return sum(i ** 2 for i in range(n))

print(expensive_calc(1000))  # 计算 1000...
print(expensive_calc(1000))  # 直接返回缓存
```

---

## 4. 简单装饰器原理

### 说明
装饰器本质上就是一个高阶函数，接收函数返回新函数。@语法糖只是语法便利。

### 示例
```python
def timer(func):
    """计时装饰器"""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时: {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "done"

# 等同于: slow_function = timer(slow_function)
result = slow_function()
print(result)
```

### 常见错误
```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def greet(name):
    """问候函数"""
    return f"你好, {name}"

print(greet.__name__)  # 'wrapper' — 函数名被覆盖了！
# 解决：用 functools.wraps
```

---

## 总结

| 概念 | 说明 |
|------|------|
| LEGB | 变量查找顺序 |
| global | 声明全局变量 |
| nonlocal | 声明外层函数变量 |
| 闭包 | 内部函数 + 外部变量引用 |
| 装饰器 | 语法糖，本质是高阶函数 |
