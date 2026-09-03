# Day 45 课程：设计模式

## 第一部分：创建型模式

### 1.1 Singleton（单例）

`python
# Pythonic 方式：模块级实例
# config.py
class _Config:
    def __init__(self):
        self.debug = False
        self.db_url = 'sqlite:///app.db'

config = _Config()  # 模块导入天然单例

# 使用
from config import config
config.debug = True
`

`python
# 装饰器方式
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connection = None
`

### 1.2 Factory

`python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data): ...

class LocalStorage(Storage):
    def save(self, data):
        with open('data.json', 'w') as f:
            json.dump(data, f)

class S3Storage(Storage):
    def save(self, data):
        # S3 上传逻辑
        pass

class StorageFactory:
    @staticmethod
    def create(storage_type: str) -> Storage:
        if storage_type == 'local':
            return LocalStorage()
        elif storage_type == 's3':
            return S3Storage()
        raise ValueError(f'Unknown storage: {storage_type}')

# 使用
storage = StorageFactory.create('local')
storage.save({'key': 'value'})
`

### 1.3 Builder

`python
class QueryBuilder:
    def __init__(self):
        self._table = ''
        self._conditions = []
        self._order = ''
        self._limit = None
    
    def table(self, name):
        self._table = name
        return self
    
    def where(self, condition):
        self._conditions.append(condition)
        return self
    
    def order_by(self, field, desc=False):
        self._order = f'ORDER BY {field} {"DESC" if desc else ""}'
        return self
    
    def limit(self, n):
        self._limit = n
        return self
    
    def build(self):
        query = f'SELECT * FROM {self._table}'
        if self._conditions:
            query += ' WHERE ' + ' AND '.join(self._conditions)
        if self._order:
            query += ' ' + self._order
        if self._limit:
            query += f' LIMIT {self._limit}'
        return query

# 使用
query = (QueryBuilder()
    .table('users')
    .where('age > 18')
    .where('active = true')
    .order_by('name')
    .limit(10)
    .build())
`

---

## 第二部分：结构型模式

### 2.1 Adapter（适配器）

`python
class OldPaymentAPI:
    def make_payment(self, amount, currency):
        return {'status': 'ok', 'amount': amount}

class NewPaymentAPI:
    def charge(self, amount_cents, currency_code):
        return {'success': True, 'total': amount_cents / 100}

class PaymentAdapter:
    """让新接口兼容旧代码"""
    def __init__(self, new_api: NewPaymentAPI):
        self.api = new_api
    
    def make_payment(self, amount, currency):
        result = self.api.charge(int(amount * 100), currency)
        return {'status': 'ok' if result['success'] else 'failed'}
`

### 2.2 Decorator（装饰器）

`python
# Python 装饰器就是设计模式
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'{func.__name__} took {time.time()-start:.4f}s')
        return result
    return wrapper

def retry(max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f'Retry {attempt + 1}: {e}')
        return wrapper
    return decorator

@timer
@retry(max_retries=3)
def fetch_data(url):
    import httpx
    resp = httpx.get(url)
    return resp.json()
`

### 2.3 Facade（外观）

`python
class OrderFacade:
    """订单系统的外观 - 简化复杂子系统交互"""
    
    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
        self.notification = NotificationService()
    
    def place_order(self, user_id, product_id, quantity):
        # 复杂流程，对外简化为一个方法
        product = self.inventory.check(product_id, quantity)
        payment = self.payment.charge(user_id, product.price * quantity)
        if not payment['success']:
            return {'error': 'Payment failed'}
        self.inventory.reserve(product_id, quantity)
        shipment = self.shipping.create(user_id, product_id, quantity)
        self.notification.send(user_id, f'Order {shipment["id"]} confirmed')
        return {'order_id': shipment['id'], 'status': 'confirmed'}
`

---

## 第三部分：行为型模式

### 3.1 Strategy（策略）

`python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data):
        return self._strategy.sort(data)
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

# 使用
sorter = Sorter(QuickSort())
result = sorter.sort([3, 1, 4, 1, 5, 9])
sorter.set_strategy(BubbleSort())  # 切换策略
`

### 3.2 Observer（观察者）

`python
class EventEmitter:
    def __init__(self):
        self._listeners = {}
    
    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)
    
    def emit(self, event, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

# 使用
emitter = EventEmitter()

emitter.on('user_created', lambda user: print(f'Welcome email sent to {user}'))
emitter.on('user_created', lambda user: print(f'Log: {user} registered'))

emitter.emit('user_created', 'Alice')
# Welcome email sent to Alice
# Log: Alice registered
`

### 3.3 State（状态）

`python
class OrderState:
    def next(self, order): ...
    def cancel(self, order): ...

class PendingState(OrderState):
    def next(self, order):
        order.state = ProcessingState()
    def cancel(self, order):
        order.state = CancelledState()

class ProcessingState(OrderState):
    def next(self, order):
        order.state = ShippedState()
    def cancel(self, order):
        order.state = CancelledState()

class ShippedState(OrderState):
    def next(self, order):
        order.state = DeliveredState()
    def cancel(self, order):
        raise ValueError("Cannot cancel shipped order")

class Order:
    def __init__(self):
        self.state = PendingState()
    
    def next(self):
        self.state.next(self)
    
    def cancel(self):
        self.state.cancel(self)
`

---

## 第四部分：何时使用/不使用

### 4.1 使用原则

- 问题存在，模式才有价值
- 简单问题不需要复杂模式
- Pythonic 优先（装饰器、上下文管理器、生成器）
- YAGNI（You Aren't Gonna Need It）

### 4.2 Python 特有的替代方案

`python
# 单例 -> 模块级变量
# 工厂 -> classmethod / __init_subclass__
# 策略 -> 函数作为一等公民
# 观察者 -> 信号库（blinker）
# 迭代器 -> 生成器
# 模板方法 -> 抽象类 + 默认实现
`

---

## 常见错误
1. 滥用设计模式 -> 过度工程
2. 为了模式而模式 -> 简单问题复杂化
3. 忽略 Python 特性 -> 用 Java 思维写 Python
4. 模式不灵活 -> 硬编码模式参数

## 动手练习
1. 实现 Observer 模式
2. 用 Strategy 模式实现不同的排序算法
3. 用 Factory 模式创建不同类型的日志 Handler
4. 用 Builder 模式构建复杂查询
