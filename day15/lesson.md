# Day 15: OOP 深入③ — 封装与property

## 1. 封装：公有/保护/私有

### 1.1 Python 的命名约定

| 前缀 | 含义 | 示例 |
|------|------|------|
| 无前缀 | 公有 | `name` |
| 单下划线 | 保护（约定） | `_name` |
| 双下划线 | 私有（名称改写） | `__name` |

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner      # 公有
        self._bank = '招商银行'  # 保护（约定，外部可访问但不建议）
        self.__balance = balance  # 私有（名称改写）

    def get_balance(self):
        return self.__balance

acc = BankAccount('Alice', 10000)
print(acc.owner)      # OK
print(acc._bank)      # OK（但不建议）
# print(acc.__balance)  # AttributeError
print(acc._BankAccount__balance)  # 10000（名称改写后的名字）
```

### 1.2 名称改写 (Name Mangling)

```python
class Private:
    def __secret(self):
        return 'secret'

    def reveal(self):
        return self.__secret()  # 内部调用没问题

p = Private()
print(p.reveal())  # 'secret'
# p.__secret()  # AttributeError
print(p._Private__secret())  # 'secret'（改写后名字）
```

---

## 2. property 深入

### 2.1 基础用法

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius  # 用保护属性存真实值

    @property
    def radius(self):
        '''getter: 读取时调用'''
        return self._radius

    @radius.setter
    def radius(self, value):
        '''setter: 赋值时调用'''
        if value < 0:
            raise ValueError('半径不能为负')
        self._radius = value

    @radius.deleter
    def radius(self):
        '''deleter: 删除时调用'''
        print('删除半径')
        del self._radius

    @property
    def area(self):
        '''只读属性（没有setter）'''
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)    # 5（调用getter）
print(c.area)      # 78.54（只读）
c.radius = 10      # 调用setter
# c.radius = -1    # ValueError
# c.area = 100     # AttributeError（只读）
```

### 2.2 常见模式

```python
class User:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name

    # 计算属性
    @property
    def full_name(self):
        return f'{self._first_name} {self._last_name}'

    # 用setter同步更新
    @full_name.setter
    def full_name(self, value):
        parts = value.split(' ', 1)
        self._first_name = parts[0]
        self._last_name = parts[1] if len(parts) > 1 else ''

    # 缓存属性
    @property
    def expensive_data(self):
        if not hasattr(self, '_cached_data'):
            print('计算中...')
            self._cached_data = sum(range(1000000))
        return self._cached_data

u = User('John', 'Doe')
print(u.full_name)  # 'John Doe'
u.full_name = 'Jane Smith'
print(u._first_name)  # 'Jane'
```

### 2.3 property 继承

```python
class Base:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

class Child(Base):
    @property
    def value(self):
        '''覆盖getter，添加日志'''
        print('reading value')
        return super().value

    @value.setter
    def value(self, v):
        '''覆盖setter，添加验证'''
        if v < 0:
            raise ValueError('不能为负')
        super(Child, self.__class__).value.fset(self, v)
```

---

## 3. 描述符深入

### 3.1 数据描述符 vs 非数据描述符

```python
# 数据描述符: 实现 __set__ 或 __delete__
# 非数据描述符: 只实现 __get__

# 优先级:
# 数据描述符 > 实例 __dict__ > 非数据描述符

class DataDesc:
    def __get__(self, obj, objtype=None):
        return 'data descriptor'
    def __set__(self, obj, value):
        print(f'data desc set: {value}')

class NonDataDesc:
    def __get__(self, obj, objtype=None):
        return 'non-data descriptor'

class Test:
    data = DataDesc()
    nondata = NonDataDesc()

t = Test()
t.data = 'test'    # 触发数据描述符
t.__dict__['data'] = 'instance'  # 不会覆盖数据描述符
print(t.data)       # 'data descriptor'

t.nondata = 'test'  # 直接写入 __dict__
print(t.nondata)    # 'test'（实例属性遮蔽了非数据描述符）
```

### 3.2 描述符实现缓存

```python
class Cached:
    def __init__(self, func):
        self.func = func
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = f'_cached_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.attr_name):
            setattr(obj, self.attr_name, self.func(obj))
        return getattr(obj, self.attr_name)

class DataProcessor:
    def __init__(self, data):
        self.data = data

    @Cached
    def expensive_result(self):
        print('计算中...')
        return sum(x ** 2 for x in self.data)

p = DataProcessor(range(1000))
print(p.expensive_result)  # 计算中... 332833500
print(p.expensive_result)  # 332833500（缓存，不重新计算）
```

---

## 4. classmethod 工厂方法

### 4.1 多种构造方式

```python
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['age'], data['email'])

    @classmethod
    def from_string(cls, s):
        name, age, email = s.split(',')
        return cls(name, int(age), email)

    @classmethod
    def anonymous(cls, age):
        return cls('Anonymous', age, '')

u1 = User.from_dict({'name': 'Alice', 'age': 25, 'email': 'a@b.com'})
u2 = User.from_string('Bob,30,b@b.com')
u3 = User.anonymous(20)
```

### 4.2 继承中的工厂方法

```python
class Animal:
    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name):
        return cls(name)

class Dog(Animal):
    pass

class Cat(Animal):
    pass

d = Dog.create('旺财')  # 自动创建 Dog 实例
c = Cat.create('咪咪')  # 自动创建 Cat 实例
print(type(d))  # <class 'Dog'>
```

---

## 5. 数据验证系统

### 5.1 完整验证框架

```python
class Validator:
    def __init__(self, **rules):
        self.rules = rules

    def validate(self, data):
        errors = []
        for field, rules in self.rules.items():
            value = data.get(field)
            for rule in rules:
                if rule == 'required' and value is None:
                    errors.append(f'{field} is required')
                elif isinstance(rule, tuple) and rule[0] == 'type':
                    if value is not None and not isinstance(value, rule[1]):
                        errors.append(f'{field} must be {rule[1].__name__}')
        return errors

user_validator = Validator(
    name=['required', (str, )],
    age=['required', (int, )],
    email=['required'],
)

errors = user_validator.validate({'name': 'Alice', 'age': '25'})
print(errors)  # ['age must be int']
```

---

## 本日总结

| 概念 | 一句话 |
|------|--------|
| 私有属性 | 双下划线触发名称改写 |
| property | 用装饰器定义 getter/setter |
| 数据描述符 | 实现 __set__，优先于实例属性 |
| classmethod | 工厂方法，cls 自动传入类 |
| 缓存描述符 | 避免重复计算 |
