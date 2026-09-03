# Day 13: OOP 深入① — 类的深层机制

## 1. 实例属性 vs 类属性

### 1.1 核心概念

类属性属于**类本身**，所有实例共享；实例属性属于**具体实例**，每个实例独立。

```
类属性: 定义在class体内、方法外面
实例属性: 在__init__中通过self.xxx = value定义
```

### 1.2 属性查找机制

Python 查找属性的顺序：
1. 实例的 `__dict__`
2. 类的 `__dict__`
3. 父类的 `__dict__`（按MRO顺序）

```python
class Dog:
    species = '犬科'  # 类属性

    def __init__(self, name, age):
        self.name = name    # 实例属性
        self.age = age      # 实例属性

buddy = Dog('Buddy', 3)
print(buddy.species)   # '犬科' -- 找到类属性
print(buddy.name)      # 'Buddy' -- 找到实例属性

# 关键：赋值创建实例属性，遮蔽类属性
buddy.species = '柴犬'
print(buddy.species)   # '柴犬' -- 实例属性
print(Dog.species)     # '犬科' -- 类属性没变！

# 改类属性必须通过类
Dog.species = '哺乳纲'
print(buddy.species)   # 现在是 '哺乳纲'
```

### 1.3 常见陷阱：可变类属性

```python
class Team:
    members = []  # 所有实例共享！

    def __init__(self, name):
        self.name = name

t1 = Team('A')
t2 = Team('B')
t1.members.append('Alice')
print(t2.members)  # ['Alice'] -- 意外共享！

# 正确做法
class TeamFixed:
    def __init__(self, name):
        self.name = name
        self.members = []  # 每个实例独立
```

### 1.4 常见错误

| 错误 | 正确 |
|------|------|
| 以为 `obj.attr = value` 改类属性 | 这只改实例属性 |
| `items = []` 做类属性默认值 | 在 `__init__` 中初始化 |
| 忽略可变共享问题 | 每个实例独立初始化 |

### 1.5 动手练习
创建 Student 类，类属性 `total_count` 自动计数，每次创建 +1，删除 -1。

---

## 2. 方法类型

### 2.1 实例方法
- 第一个参数是 `self`（实例本身）
- 能访问实例属性和类属性

```python
class Cat:
    def __init__(self, name):
        self.name = name

    def meow(self):  # 实例方法
        return f'{self.name}: 喵~'

cat = Cat('咪咪')
print(cat.meow())  # '咪咪: 喵~'
```

### 2.2 类方法 (@classmethod)
- 第一个参数是 `cls`（类本身）
- 常用于工厂方法、替代构造函数

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        from datetime import date
        d = date.today()
        return cls(d.year, d.month, d.day)

d = Date.from_string('2024-03-15')
print(d.year)  # 2024
```

### 2.3 静态方法 (@staticmethod)
- 没有 `self` 也没有 `cls`
- 本质是放在类里的普通函数

```python
class MathHelper:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))

print(MathHelper.is_even(4))       # True
print(MathHelper.clamp(15, 0, 10)) # 10
```

### 2.4 三种方法对比

| 类型 | 装饰器 | 第一个参数 | 访问实例属性 | 典型用途 |
|------|--------|-----------|-------------|---------|
| 实例方法 | 无 | self | 可以 | 操作实例数据 |
| 类方法 | @classmethod | cls | 不行 | 工厂方法 |
| 静态方法 | @staticmethod | 无 | 不行 | 工具函数 |
---

## 3. 构造函数链

### 3.1 __init_subclass__

子类被定义时自动触发，常用于插件注册。

```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower()
        Plugin._registry[name] = cls

class AudioPlugin(Plugin, plugin_name='audio'):
    pass

class VideoPlugin(Plugin, plugin_name='video'):
    pass

print(Plugin._registry)
# {'audio': <class 'AudioPlugin'>, 'video': <class 'VideoPlugin'>}
```

### 3.2 super() 的真相

`super()` 不是"调父类"，是按 MRO 顺序调"下一个"。

```python
class A:
    def __init__(self):
        print('A')

class B(A):
    def __init__(self):
        print('B')
        super().__init__()

class C(A):
    def __init__(self):
        print('C')
        super().__init__()

class D(B, C):  # MRO: D -> B -> C -> A
    def __init__(self):
        print('D')
        super().__init__()

D()
# 输出: D -> B -> C -> A
```

### 3.3 常见错误

```python
# 错误: 直接调父类（破坏MRO）
class Bad(B):
    def __init__(self):
        B.__init__(self)  # 不推荐

# 正确: 用super()
class Good(B):
    def __init__(self):
        super().__init__()  # 推荐
```

---

## 4. 描述符基础

### 4.1 什么是描述符

实现了 `__get__`、`__set__`、`__delete__` 中任一方法的对象就是描述符。

```python
class Validated:
    """数据验证描述符"""

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name  # 自动获取属性名

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f'{self.name} 不能小于 {self.min_value}')
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f'{self.name} 不能大于 {self.max_value}')
        obj.__dict__[self.name] = value

class Student:
    age = Validated(min_value=0, max_value=150)
    score = Validated(min_value=0, max_value=100)

    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('小明', 15, 95)
# s.age = -5    # ValueError: age 不能小于 0
# s.score = 200 # ValueError: score 不能大于 100
```

### 4.2 数据描述符 vs 非数据描述符

- **数据描述符**: 实现了 `__set__` 或 `__delete__`
- **非数据描述符**: 只实现了 `__get__`

数据描述符优先级高于实例 `__dict__`，这就是为什么 `@property` 能拦截赋值。

### 4.3 property 本质是描述符

`@property`、`@xxx.setter`、`@xxx.deleter` 就是内置的数据描述符。
---

## 5. __slots__

### 5.1 核心概念

`__slots__` 限制实例只能有指定属性，禁止动态添加，节省内存。

```python
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.x, p.y)
# p.z = 3  # AttributeError: 'Point' object has no attribute 'z'
```

### 5.2 内存对比

```python
import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlotPoint:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

rp = RegularPoint(1, 2)
sp = SlotPoint(1, 2)
print(sys.getsizeof(rp.__dict__))  # 104 bytes
# sp 没有 __dict__，节省大量内存
# 百万级对象差距巨大
```

### 5.3 继承中的 slots

```python
class Base:
    __slots__ = ('x',)

class Child(Base):
    __slots__ = ('y',)  # 不重复父类的

c = Child()
c.x = 1  # OK
c.y = 2  # OK
```

### 5.4 注意事项

- `__slots__` 类不能用 `**kwargs` 动态属性
- 和 `__dict__` 默认互斥（除非显式加 `__dict__`）
- 多继承时小心 slots 冲突
- 不加 `__slots__` 的父类会让 slots 失效

---

## 6. 实例生命周期

### 6.1 完整流程

```
__new__(cls)     --> 创建实例（分配内存）
__init__(self)   --> 初始化实例
  ... 使用中 ...
__del__(self)    --> 销毁实例
```

### 6.2 代码示例

```python
class Lifecycle:
    def __new__(cls, *args, **kwargs):
        print(f'1. __new__ 被调用，args={args}')
        instance = super().__new__(cls)
        return instance

    def __init__(self, name):
        print(f'2. __init__ 被调用，name={name}')
        self.name = name

    def __del__(self):
        print(f'3. __del__ 被调用，{self.name} 被销毁')

obj = Lifecycle('测试')
# 输出:
# 1. __new__ 被调用，args=('测试',)
# 2. __init__ 被调用，name=测试

del obj
# 输出: 3. __del__ 被调用，测试 被销毁
```

### 6.3 __new__ 实际用途：单例模式

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)  # True -- 同一个对象
```

### 6.4 不可变类型必须在 __new__ 设属性

```python
class FrozenPoint:
    def __new__(cls, x, y):
        inst = super().__new__(cls)
        object.__setattr__(inst, '_x', x)
        object.__setattr__(inst, '_y', y)
        return inst

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

p = FrozenPoint(3, 4)
print(p.x, p.y)
# p.x = 5  # AttributeError -- 不可变
```

### 6.5 常见错误

```python
# 错误: 在__init__里返回值
class Bad:
    def __init__(self):
        return 'something'  # TypeError!

# __new__ 可以返回非本类实例（用于单例等）
```

---

## 7. 组合 vs 继承

### 7.1 选择原则

- **继承**: "is-a" 关系（Dog is Animal）
- **组合**: "has-a" 关系（Car has Engine）

### 7.2 继承示例

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return '汪!'

class Cat(Animal):
    def speak(self):
        return '喵~'

for animal in [Dog('旺财'), Cat('咪咪')]:
    print(f'{animal.name}: {animal.speak()}')
```

### 7.3 组合示例

```python
class Engine:
    def __init__(self, hp):
        self.hp = hp
    def start(self):
        return f'{self.hp}马力引擎启动'

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine  # has-a

    def start(self):
        return f'{self.brand}: {self.engine.start()}'

car = Car('宝马', Engine(300))
print(car.start())  # '宝马: 300马力引擎启动'
```

### 7.4 决策表

| 场景 | 推荐 | 原因 |
|------|------|------|
| 动物/形状/角色 | 继承 | 天然类型层次 |
| 配置/工具/服务 | 组合 | 灵活替换 |
| 多维度扩展 | 组合+Mixin | 避免钻石继承 |
| 代码复用 | 组合优先 | 低耦合 |

### 7.5 实际应用：策略模式

```python
class Sorter:
    def __init__(self, strategy=None):
        self._strategy = strategy or sorted

    def sort(self, data):
        return self._strategy(data)

# 可替换排序策略
sorter = Sorter(strategy=lambda d: sorted(d, reverse=True))
print(sorter.sort([3, 1, 2]))  # [3, 2, 1]

# 换策略
sorter._strategy = sorted
print(sorter.sort([3, 1, 2]))  # [1, 2, 3]
```

---

## 本日总结

| 概念 | 一句话 |
|------|--------|
| 类属性 | 所有实例共享，通过类名访问 |
| 实例属性 | 每个实例独立，通过 self 赋值 |
| 实例方法 | 操作实例数据，self 是第一个参数 |
| 类方法 | 工厂方法，cls 是第一个参数 |
| 静态方法 | 工具函数，不访问类或实例 |
| 描述符 | 实现 __get__/__set__ 的对象，控制属性访问 |
| __slots__ | 限制属性，节省内存 |
| 生命周期 | __new__ -> __init__ -> 使用 -> __del__ |
| 组合 vs 继承 | has-a 用组合，is-a 用继承 |
