# Day 13 挑战 — 类的深层机制

## Challenge 1: 学生计数器
**目标**: 用类属性实现自动计数

**要求**:
1. 创建 `Student` 类
2. 类属性 `total_count` 自动追踪学生数量
3. 每次创建实例 +1，删除实例 -1（用 `__del__`）
4. 实例属性: name, age, scores（列表）
5. 方法: `average_score()` 返回平均分

**示例**:
```python
print(Student.total_count)  # 0
s1 = Student('Alice', 20, [90, 85, 92])
s2 = Student('Bob', 21, [78, 82, 85])
print(Student.total_count)  # 2
del s1
print(Student.total_count)  # 1
```

---

## Challenge 2: 方法类型大练习
**目标**: 熟练使用三种方法类型

**要求**:
1. 创建 `Temperature` 类
2. 实例方法 `to_fahrenheit()`: 摄氏转华氏
3. 类方法 `from_fahrenheit(cls, f)`: 从华氏创建实例
4. 类方法 `from_string(cls, s)`: 从 "36.5C" 或 "97.7F" 字符串创建
5. 静态方法 `is_freezing(celsius)`: 判断是否低于0度

**示例**:
```python
t = Temperature(36.5)
print(t.to_fahrenheit())  # 97.7
t2 = Temperature.from_fahrenheit(97.7)
print(t2.celsius)  # 36.5
t3 = Temperature.from_string('0C')
print(Temperature.is_freezing(t3.celsius))  # True
```

---

## Challenge 3: 描述符验证
**目标**: 用描述符做属性验证

**要求**:
1. 创建 `ValidatedField` 描述符
2. 支持: min_value, max_value, required, type_check
3. 用 `__set_name__` 自动获取属性名
4. 创建 `Product` 类使用:
   - `name` = ValidatedField(required=True, type_check=str)
   - `price` = ValidatedField(min_value=0.01, type_check=float)
   - `stock` = ValidatedField(min_value=0, type_check=int)

**示例**:
```python
p = Product('iPhone', 999.99, 100)  # OK
# Product('', 999.99, 100)  # ValueError: name is required
# Product('iPhone', -1, 100)  # ValueError: price must be >= 0.01
```

---

## Challenge 4: 单例 + slots
**目标**: 结合单例模式和 slots

**要求**:
1. 创建 `Config` 单例类
2. 用 `__slots__` 限制属性: db_host, db_port, db_name, debug
3. `__new__` 实现单例
4. 支持 `update(**kwargs)` 更新配置
5. 支持 `reset()` 重置为默认值

**示例**:
```python
c1 = Config()
c1.db_host = 'localhost'
c1.debug = True
c2 = Config()
print(c1 is c2)  # True
print(c2.db_host)  # 'localhost'
c2.reset()
print(c2.db_host)  # None
```

---

## Challenge 5: 组合 vs 继承
**目标**: 用组合+继承设计灵活系统

**要求**:
1. 创建 `Logger` mixin（提供 `log(msg)` 方法）
2. 创建 `Serializable` mixin（提供 `to_dict()` 方法）
3. 创建 `Database` 基类（用组合包含 Logger）
4. 创建 `MySQL` 和 `PostgreSQL` 继承 Database
5. 每个数据库类支持: connect(), disconnect(), query(sql)

**示例**:
```python
db = MySQL(host='localhost', port=3306)
db.connect()
db.log('Connected!')  # [MySQL] Connected!
result = db.query('SELECT * FROM users')
print(db.to_dict())  # {'type': 'MySQL', 'host': 'localhost', ...}
```
