# Day 17: dataclass

## 1. @dataclass 基础

### 1.1 为什么需要 dataclass

手写 `__init__`, `__repr__`, `__eq__` 很烦，dataclass 自动生成。

```python
# 手写版本
class PointManual:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'PointManual(x={self.x}, y={self.y})'
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# dataclass 版本
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    # 自动生成 __init__, __repr__, __eq__
```

### 1.2 自动生成的方法

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

u = User('Alice', 25, 'alice@example.com')
print(u)           # User(name='Alice', age=25, email='alice@example.com')
print(u == User('Alice', 25, 'alice@example.com'))  # True
```

---

## 2. field() 高级

### 2.1 默认值

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str = 'localhost'
    port: int = 8080
    debug: bool = False
    tags: list = field(default_factory=list)  # 可变默认值必须用 default_factory
    _secret: str = field(default='***', repr=False)  # 不显示在 repr 中

c = Config()
print(c)  # Config(host='localhost', port=8080, debug=False, tags=[], _secret='***')
# 注意: _secret 不会显示（因为 repr=False）
```

### 2.2 field() 参数

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float = field(default=0.0, metadata={'unit': 'CNY'})
    stock: int = field(default=0, compare=False)  # 不参与比较
    tags: list = field(default_factory=list, hash=False)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError('价格不能为负')

p1 = Product('iPhone', 9999.0, 100, ['手机'])
p2 = Product('iPhone', 9999.0, 50, ['手机'])
print(p1 == p2)  # True -- stock 不参与比较
```

---

## 3. frozen / order / post_init

### 3.1 frozen（不可变）

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1, 2)
# p.x = 3  # FrozenInstanceError
points = {p, Point(1, 2)}
print(len(points))  # 1（可以做字典key和集合元素）
```

### 3.2 order（自动排序）

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Student:
    score: int = field(compare=True)
    name: str = field(compare=False)

students = [
    Student(90, 'Alice'),
    Student(85, 'Bob'),
    Student(95, 'Charlie'),
]
print(sorted(students))
# [Student(score=85, name='Bob'), Student(score=90, name='Alice'), ...]
```

### 3.3 __post_init__

```python
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float
    area: float = 0.0  # 计算属性

    def __post_init__(self):
        '''__init__ 后自动调用'''
        if self.radius < 0:
            raise ValueError('半径不能为负')
        self.area = 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)  # 78.54
```

---

## 4. 继承与嵌套

### 4.1 继承

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

@dataclass
class Employee(Person):
    employee_id: str
    department: str

e = Employee('Alice', 30, 'E001', 'Engineering')
print(e)  # Employee(name='Alice', age=30, employee_id='E001', department='Engineering')
```

### 4.2 嵌套 dataclass

```python
from dataclasses import dataclass, field

@dataclass
class Address:
    street: str
    city: str
    country: str = '中国'

@dataclass
class User:
    name: str
    address: Address  # 嵌套

u = User('Alice', Address('中关村大街1号', '北京'))
print(u)
# User(name='Alice', address=Address(street='中关村大街1号', city='北京', country='中国'))
```

---

## 5. __slots__

```python
from dataclasses import dataclass

@dataclass(slots=True)  # Python 3.10+
class Point:
    x: float
    y: float

p = Point(1, 2)
# p.z = 3  # AttributeError
```

---

## 6. 与 Pydantic 对比

### 6.1 原生 dataclass

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

# 无运行时类型验证
u = User(name='Alice', age='25')  # 不报错，但类型不对
```

### 6.2 Pydantic BaseModel

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# 有运行时类型验证
u = User(name='Alice', age='25')  # 自动转为 int: 25
# User(name='Alice', age='not_a_number')  # ValidationError
```

### 6.3 选择指南

| 特性 | dataclass | Pydantic |
|------|-----------|----------|
| 类型验证 | 无 | 强制 |
| JSON 序列化 | 手动 | 自动 |
| 默认值 | field() | Field() |
| 性能 | 快 | 稍慢 |
| 依赖 | 标准库 | 第三方 |
| 适用场景 | 内部数据 | API/配置 |

---

## 7. 自定义序列化

```python
from dataclasses import dataclass, asdict, astuple
import json

@dataclass
class User:
    name: str
    age: int
    scores: list = None

u = User('Alice', 25, [90, 85])
print(asdict(u))   # {'name': 'Alice', 'age': 25, 'scores': [90, 85]}
print(astuple(u))  # ('Alice', 25, [90, 85])

# JSON 序列化
json_str = json.dumps(asdict(u), ensure_ascii=False)
print(json_str)
```

---

## 本日总结

| 概念 | 一句话 |
|------|--------|
| @dataclass | 自动生成 __init__/__repr__/__eq__ |
| field() | 控制字段行为（默认值、比较、repr） |
| frozen | 不可变实例 |
| order | 自动排序 |
| __post_init__ | 初始化后处理 |
| slots | 节省内存 |
| Pydantic | 有类型验证的 dataclass |
