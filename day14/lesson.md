# Day 14: OOP 深入② — 继承体系

## 1. 继承与方法重写

### 1.1 基本继承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError('子类必须实现 speak()')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r})'

class Dog(Animal):
    def speak(self):
        return '汪!'

class Cat(Animal):
    def speak(self):
        return '喵~'

dog = Dog('旺财')
print(dog.speak())  # '汪!'
print(dog)          # Dog('旺财')
```

### 1.2 super() 的正确用法

```python
class Base:
    def __init__(self, name):
        self.name = name
        print(f'Base.__init__: {name}')

class Middle(Base):
    def __init__(self, name, age):
        super().__init__(name)  # 调用 Base.__init__
        self.age = age
        print(f'Middle.__init__: age={age}')

class Child(Middle):
    def __init__(self, name, age, score):
        super().__init__(name, age)
        self.score = score
        print(f'Child.__init__: score={score}')

c = Child('Alice', 20, 95)
# Base.__init__: Alice
# Middle.__init__: age=20
# Child.__init__: score=95
```

---

## 2. MRO (方法解析顺序)

### 2.1 什么是 MRO

Python 用 C3 线性化算法确定方法调用顺序。

```python
class A:
    def show(self): print('A')

class B(A):
    def show(self): print('B')

class C(A):
    def show(self): print('C')

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
D().show()  # B
```

### 2.2 C3 线性化规则

1. 子类优先于父类
2. 多个父类按声明顺序
3. 保持单调性

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

# MRO: D -> B -> C -> A -> object
# 规则1: D 在最前
# 规则2: B 在 C 前（声明顺序）
# 规则3: 都在 A 前
```

### 2.3 常见错误

```python
# 错误: 不一致的继承顺序
class X(Base2, Base1): pass  # 如果 Base1(Base2) 会报错
# TypeError: Cannot create a consistent method resolution order

# 查看 MRO
print(X.__mro__)
# 或
help(X)
```

---

## 3. 抽象基类 (ABC)

### 3.1 为什么需要 ABC

强制子类实现特定方法，防止忘记实现。

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        '''计算面积，子类必须实现'''
        pass

    @abstractmethod
    def perimeter(self):
        '''计算周长，子类必须实现'''
        pass

    def description(self):
        return f'{self.__class__.__name__}: 面积={self.area():.2f}'

# s = Shape()  # TypeError: Can't instantiate abstract class

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

c = Circle(5)
print(c.description())  # 'Circle: 面积=78.54'
```

### 3.2 抽象属性

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def max_speed(self):
        pass

    @abstractmethod
    def drive(self):
        pass

class Car(Vehicle):
    @property
    def max_speed(self):
        return 200

    def drive(self):
        return '驾驶汽车'

# Car(max_speed=200)  # 错误！max_speed 是抽象属性
c = Car()
print(c.max_speed)  # 200
```

### 3.3 注册虚拟子类

```python
from abc import ABC

class Flyer(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if hasattr(C, 'fly'):
            return True
        return NotImplemented

class Bird:
    def fly(self):
        return '飞行'

print(issubclass(Bird, Flyer))  # True
```

---

## 4. Mixin 模式

### 4.1 什么是 Mixin

Mixin 是一种特殊的基类，提供可复用的方法，但不单独使用。

```python
class JsonMixin:
    '''JSON 序列化 Mixin'''
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str):
        import json
        data = json.loads(json_str)
        return cls(**data)

class LogMixin:
    '''日志 Mixin'''
    def log(self, msg):
        print(f'[{self.__class__.__name__}] {msg}')

class User(JsonMixin, LogMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User('Alice', 25)
u.log('创建用户')           # [User] 创建用户
print(u.to_json())          # {"name": "Alice", "age": 25}
u2 = User.from_json('{"name": "Bob", "age": 30}')
print(u2.name)              # Bob
```

### 4.2 Mixin 设计原则

1. Mixin 不应该有 `__init__`
2. Mixin 不应该有实例属性
3. Mixin 只提供方法
4. Mixin 类名以 Mixin 结尾
5. Mixin 放在继承列表左边

### 4.3 实际应用

```python
class ComparableMixin:
    '''提供比较功能的 Mixin'''
    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

    def __lt__(self, other):
        return self.to_tuple() < other.to_tuple()

    def __le__(self, other):
        return self.to_tuple() <= other.to_tuple()

class Student(ComparableMixin):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def to_tuple(self):
        return (-self.score, self.name)  # 分数高优先

s1 = Student('Alice', 90)
s2 = Student('Bob', 85)
print(s1 > s2)  # True
```

---

## 5. 钻石继承问题

### 5.1 什么是钻石继承

```
      A
     / \
    B   C
     \ /
      D
```

### 5.2 Python 的解决方案：C3 MRO

```python
class A:
    def greet(self): return 'A'

class B(A):
    def greet(self): return 'B->' + super().greet()

class C(A):
    def greet(self): return 'C->' + super().greet()

class D(B, C):
    def greet(self): return 'D->' + super().greet()

print(D().greet())  # D->B->C->A
print(D.__mro__)
# D -> B -> C -> A -> object
# super() 按 MRO 调用，不会重复调用 A
```

### 5.3 避免钻石继承的技巧

1. 用组合代替多继承
2. 用 Mixin 代替深层继承
3. 检查 MRO: `ClassName.__mro__`

---

## 6. 类型检查

### 6.1 isinstance 和 issubclass

```python
class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

dog = Dog()
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True -- 继承链
print(isinstance(dog, Cat))     # False

print(issubclass(Dog, Animal))  # True
```

### 6.2 type vs isinstance

```python
# type: 精确类型匹配
# isinstance: 匹配类型及所有子类

print(type(dog) == Dog)          # True
print(type(dog) == Animal)       # False
print(isinstance(dog, Animal))  # True

# 推荐: 99% 的情况用 isinstance
```

### 6.3鸭子类型 (Duck Typing)

```python
# Python 推荐: 不检查类型，检查行为
class Duck:
    def quack(self): return '嘎嘎'
    def swim(self): return '游泳'

class Person:
    def quack(self): return '学鸭叫'
    def swim(self): return '狗刨'

def duck_test(obj):
    # 不关心类型，只关心有 quack 和 swim
    print(obj.quack(), obj.swim())

duck_test(Duck())    # 嘎嘎 游泳
duck_test(Person())  # 学鸭叫 狗刨
```

### 6.4 Protocol (Python 3.8+)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return '○'

def render(obj: Drawable):
    print(obj.draw())

render(Circle())  # OK -- 不需要显式继承
```

---

## 本日总结

| 概念 | 一句话 |
|------|--------|
| MRO | C3 线性化决定方法查找顺序 |
| super() | 按 MRO 调用"下一个"类 |
| ABC | 强制子类实现接口 |
| Mixin | 可复用的方法集合 |
| 钻石继承 | C3 MRO 解决重复调用 |
| isinstance | 检查继承链 |
| 鸭子类型 | 不看类型看行为 |
