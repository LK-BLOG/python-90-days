# Day 46 课程：SOLID原则

## 第一部分：SOLID概述

### 1.1 什么是SOLID

SOLID是面向对象设计的五大基本原则，由Robert C. Martin（Uncle Bob）提出。它们的目标是让代码**可维护、可扩展、可理解**。

记住：SOLID不是教条，是工具。不是所有代码都需要严格遵循，但当代码开始发臭时，回头看看SOLID往往能找到答案。

### 1.2 为什么Python需要SOLID

Python是动态语言，很多人觉得"SOLID是Java那帮人的事"。错。

Python不强制你用接口、抽象类，但这恰恰意味着你更容易写出违反SOLID的代码。没有编译器帮你把关，代码质量全靠自觉。

---

## 第二部分：S — 单一职责原则（Single Responsibility Principle）

### 2.1 定义
> 一个类应该只有一个引起它变化的原因。

换句话说：一个类/模块/函数只干一件事。

### 2.2 违反SRP的例子
`python
class Employee:
    """违反SRP：计算工资 + 保存到数据库 + 生成报告"""
    
    def calculate_pay(self) -> float:
        """计算工资 — 这是一个职责"""
        return self.salary * self.tax_rate
    
    def save_to_database(self) -> None:
        """保存到数据库 — 这是另一个职责"""
        db.execute("INSERT INTO employees ...")
    
    def generate_report(self) -> str:
        """生成报告 — 这又是另一个职责"""
        return f"Report for {self.name}"
    
    def send_email(self, message: str) -> None:
        """发邮件 — 还是另一个职责"""
        email_client.send(self.email, message)
`

**问题：** 修改报告格式可能影响保存逻辑，修改数据库Schema可能影响工资计算。四个职责耦合在一起，改一个可能炸三个。

### 2.3 遵循SRP的重构
`python
class Employee:
    """只管员工数据"""
    def __init__(self, name: str, salary: float, tax_rate: float):
        self.name = name
        self.salary = salary
        self.tax_rate = tax_rate

class PayCalculator:
    """只管算工资"""
    def calculate(self, employee: Employee) -> float:
        return employee.salary * employee.tax_rate

class EmployeeRepository:
    """只管持久化"""
    def save(self, employee: Employee) -> None:
        db.execute("INSERT INTO employees ...", employee.name)

class ReportGenerator:
    """只管生成报告"""
    def generate(self, employee: Employee) -> str:
        return f"Report for {employee.name}"

class EmailService:
    """只管发邮件"""
    def send(self, to: str, message: str) -> None:
        email_client.send(to, message)
`

**好处：** 每个类只因一种原因变化。改报告格式？只动ReportGenerator。换数据库？只动EmployeeRepository。

---

## 第三部分：O — 开闭原则（Open/Closed Principle）

### 3.1 定义
> 软件实体应该对扩展开放，对修改关闭。

加新功能时，应该**添加新代码**而不是**修改已有代码**。

### 3.2 违反OCP的例子
`python
class DiscountCalculator:
    def calculate(self, customer_type: str, amount: float) -> float:
        if customer_type == "regular":
            return amount * 0.9
        elif customer_type == "premium":
            return amount * 0.8
        elif customer_type == "vip":
            return amount * 0.7
        # 每加一种客户类型，就要改这个方法
        elif customer_type == "new":
            return amount * 0.95
`

**问题：** 每新增一种客户类型，都要修改这个方法。改已有代码 = 引入bug的风险。

### 3.3 遵循OCP的重构
`python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """折扣策略抽象"""
    @abstractmethod
    def calculate(self, amount: float) -> float:
        ...

class RegularDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.9

class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.8

class VipDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.7

class NewCustomerDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.95

class DiscountCalculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy
    
    def calculate(self, amount: float) -> float:
        return self.strategy.calculate(amount)
`

**好处：** 新增客户类型？写一个新类完事。完全不用改已有代码。

---

## 第四部分：L — 里氏替换原则（Liskov Substitution Principle）

### 4.1 定义
> 子类型必须能够替换其基类型，且不改变程序的正确性。

说人话：凡是父类能用的地方，子类换了也得能正常工作。

### 4.2 经典违反：正方形-长方形问题
`python
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def set_width(self, width: float) -> None:
        self.width = width
    
    def set_height(self, height: float) -> None:
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Rectangle):
    """看起来合理：正方形是特殊的长方形"""
    def set_width(self, width: float) -> None:
        self.width = width
        self.height = width  # 强制宽高相等
    
    def set_height(self, height: float) -> None:
        self.width = height  # 强制宽高相等
        self.height = height

def print_area(rect: Rectangle) -> None:
    rect.set_width(5)
    rect.set_height(4)
    print(f"Expected: 20, Got: {rect.area()}")

print_area(Rectangle(0, 0))  # Expected: 20, Got: 20 ✓
print_area(Square(0, 0))     # Expected: 20, Got: 16 ✗ ← 违反LSP！
`

### 4.3 正确的做法
`python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2
`

**核心：** 不要为了复用代码强行建立继承关系。如果子类的行为和父类不一致，就别继承。

---

## 第五部分：I — 接口隔离原则（Interface Segregation Principle）

### 5.1 定义
> 不应该强迫客户端依赖它不使用的接口。

### 5.2 违反ISP的例子
`python
class Worker(ABC):
    @abstractmethod
    def work(self) -> None: ...
    
    @abstractmethod
    def eat(self) -> None: ...
    
    @abstractmethod
    def sleep(self) -> None: ...

class Robot(Worker):
    def work(self) -> None:
        print("Robot working")
    
    def eat(self) -> None:
        raise NotImplementedError("Robots don't eat!")  # 被迫实现不需要的方法
    
    def sleep(self) -> None:
        raise NotImplementedError("Robots don't sleep!")
`

### 5.3 遵循ISP的重构
`python
class Workable(ABC):
    @abstractmethod
    def work(self) -> None: ...

class Feedable(ABC):
    @abstractmethod
    def eat(self) -> None: ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self) -> None: ...

class HumanWorker(Workable, Feedable, Sleepable):
    """人类工人：工作、吃饭、睡觉"""
    def work(self): print("Working")
    def eat(self): print("Eating")
    def sleep(self): print("Sleeping")

class Robot(Workable):
    """机器人：只工作，不吃不睡"""
    def work(self): print("Robot working")
`

---

## 第六部分：D — 依赖倒置原则（Dependency Inversion Principle）

### 6.1 定义
> 高层模块不应该依赖低层模块，两者都应该依赖抽象。
> 抽象不应该依赖细节，细节应该依赖抽象。

### 6.2 违反DIP的例子
`python
class MySQLDatabase:
    def save(self, data: dict) -> None:
        # MySQL specific code
        pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # 直接依赖具体实现
    
    def save_user(self, user: dict) -> None:
        self.db.save(user)
`

**问题：** 想换PostgreSQL？改UserService。想测试？mock MySQL很痛苦。

### 6.3 遵循DIP的重构
`python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data: dict) -> None: ...

class MySQLDatabase(Database):
    def save(self, data: dict) -> None:
        print(f"Saving to MySQL: {data}")

class PostgresDatabase(Database):
    def save(self, data: dict) -> None:
        print(f"Saving to PostgreSQL: {data}")

class UserService:
    def __init__(self, db: Database):  # 依赖抽象
        self.db = db
    
    def save_user(self, user: dict) -> None:
        self.db.save(user)

# 使用
service = UserService(MySQLDatabase())  # 想换？改成PostgresDatabase()
`

---

## 第七部分：反模式识别

### 7.1 God Object（上帝对象）
一个类啥都干，几百上千行，修改它像在雷区走路。
`python
# 反模式：God Object
class AppManager:
    def handle_request(self): ...
    def process_payment(self): ...
    def send_email(self): ...
    def generate_report(self): ...
    def manage_users(self): ...
    def handle_database(self): ...
    # ... 还有50个方法
`

### 7.2 Feature Envy（依恋情结）
一个类的方法频繁访问另一个类的数据，它可能应该搬到那个类里去。
`python
# 反模式：Feature Envy
class OrderPrinter:
    def print_order(self, order: Order):
        # 大量访问order的内部数据
        print(f"Customer: {order.customer.name}")
        print(f"Email: {order.customer.email}")
        print(f"Total: {order.calculate_total()}")
        for item in order.items:
            print(f"  {item.product.name}: {item.quantity} x {item.price}")
`
→ 这些逻辑应该在Order类里。

### 7.3 Primitive Obsession（基本类型偏执）
用字符串、数字等基本类型代替小对象。
`python
# 反模式
def create_user(name: str, email: str, phone: str, address: str, city: str, country: str):
    # 六个字符串参数，哪个是哪个？

# 改进
def create_user(name: str, email: Email, phone: PhoneNumber, address: Address):
    # 每个参数有明确的类型和验证
`

### 7.4 Switch/If-Else链
`python
# 反模式
def get_shipping_cost(country: str, weight: float) -> float:
    if country == "CN":
        return weight * 2
    elif country == "US":
        return weight * 5
    elif country == "JP":
        return weight * 4
    # 每加一个国家就加一个elif...
`
→ 策略模式解决。

---

## 第八部分：Python特色 — 不需要教条地用SOLID

Python的优势：不需要像Java那样为每个原则都搞出一堆接口和抽象类。

### 8.1 Pythonic的SOLID
`python
# Python的鸭子类型天然支持OCP和LCP
# 不需要显式声明接口，只要实现了对应方法就行

class PdfExporter:
    def export(self, data: dict) -> bytes:
        return f"PDF: {data}".encode()

class CsvExporter:
    def export(self, data: dict) -> bytes:
        return f"CSV: {data}".encode()

# 只要有export方法，任何对象都能传进来
def generate_report(exporter, data):
    return exporter.export(data)
`

### 8.2 Protocol — Python的结构化子类型（LSP的Pythonic实现）
`python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "○"

class Square:
    def draw(self) -> str:
        return "□"

def render(shape: Drawable) -> None:
    print(shape.draw())

# Circle和Square不需要继承任何东西
# 只要有draw方法，Protocol就认可
render(Circle())  # OK
render(Square())  # OK
`

---

## 课堂练习

### 练习：找出违反的SOLID原则
`python
class DataProcessor:
    def read_csv(self, path: str) -> list[dict]:
        ...
    
    def validate_data(self, data: list[dict]) -> bool:
        ...
    
    def transform_data(self, data: list[dict]) -> list[dict]:
        ...
    
    def save_to_db(self, data: list[dict]) -> None:
        ...
    
    def send_notification(self, message: str) -> None:
        ...
`

**答：** 主要是SRP违反 — 一个类干了5件不相关的事。
OCP也有问题 — 如果要支持新的数据源（JSON/Excel），必须修改这个类。

---

## 本课总结

| 原则 | 核心思想 | Python实践 |
|------|---------|-----------|
| SRP | 一个类只干一件事 | 拆分职责到不同模块 |
| OCP | 对扩展开放，对修改关闭 | 策略模式、Protocol、鸭子类型 |
| LSP | 子类能替换父类 | 测试、Protocol而非继承 |
| ISP | 接口要小而专 | 多个Protocol组合 |
| DIP | 依赖抽象不依赖具体 | 构造函数注入、Protocol |

**下一课预告：** Day 47 将学习依赖注入和IoC容器，把DIP原则落地。
