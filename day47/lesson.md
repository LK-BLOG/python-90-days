# Day 47 课程：依赖注入 & IoC

## 第一部分：什么是依赖注入

### 1.1 核心概念

**依赖（Dependency）：** 一个对象需要另一个对象才能工作。
**注入（Injection）：** 把依赖"塞进去"，而不是让对象自己去找。

`python
# 没有DI：自己创建依赖
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # 硬编码依赖

# 有DI：外部注入依赖
class UserService:
    def __init__(self, db: Database):
        self.db = db  # 依赖从外部传入
`

### 1.2 控制反转（IoC）

IoC是DI的理论基础。传统编程中，你控制对象的创建流程；IoC把这个控制权交给外部容器。

`
传统：User → 创建 → Database
IoC：  User ← 注入 ← 容器
`

### 1.3 为什么需要DI
1. **可测试性** — 测试时注入mock对象
2. **可替换性** — 换实现不改代码
3. **可配置性** — 不同环境不同配置
4. **解耦** — 模块之间不直接依赖

---

## 第二部分：手动DI

### 2.1 构造函数注入（推荐）
`python
class EmailSender:
    def __init__(self, smtp_host: str, smtp_port: int):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

class UserService:
    def __init__(self, db: Database, email_sender: EmailSender):
        self.db = db
        self.email = email_sender

# 组装
db = PostgresDatabase(config.DB_URL)
email = EmailSender(config.SMTP_HOST, config.SMTP_PORT)
user_service = UserService(db, email)
`

### 2.2 方法注入
`python
class ReportService:
    def generate(self, data: list, formatter: Formatter) -> str:
        return formatter.format(data)

# 每次调用时传入不同formatter
report = service.generate(data, PdfFormatter())
report = service.generate(data, HtmlFormatter())
`

### 2.3 属性注入
`python
class CacheService:
    cache: Cache  # 外部设置

cache_service = CacheService()
cache_service.cache = RedisCache()  # 属性注入
`
→ 不推荐：太松散，容易忘记设置。

---

## 第三部分：DI容器

### 3.1 什么是DI容器
DI容器是一个负责：
- 管理对象的生命周期
- 自动解析依赖关系
- 提供配置驱动的对象创建

### 3.2 手写简单DI容器
`python
from typing import Any, Callable, Type, TypeVar

T = TypeVar("T")

class Container:
    def __init__(self):
        self._bindings: dict[str, Callable] = {}
        self._singletons: dict[str, Any] = {}

    def bind(self, interface: str, factory: Callable) -> None:
        self._bindings[interface] = factory

    def singleton(self, interface: str, factory: Callable) -> None:
        def wrapper():
            if interface not in self._singletons:
                self._singletons[interface] = factory()
            return self._singletons[interface]
        self._bindings[interface] = wrapper

    def resolve(self, interface: str) -> Any:
        if interface not in self._bindings:
            raise KeyError(f"No binding for {interface}")
        return self._bindings[interface]()

# 使用
container = Container()
container.bind("database", lambda: PostgresDatabase(config.DB_URL))
container.bind("cache", lambda: RedisCache(config.REDIS_URL))

# 注册UserService的工厂，它会自动解析依赖
container.bind("user_service", lambda: UserService(
    db=container.resolve("database"),
    cache=container.resolve("cache"),
))

# 使用
user_service = container.resolve("user_service")
`

---

## 第四部分：dependency-injector框架

### 4.1 安装
`ash
pip install dependency-injector
`

### 4.2 基本概念
- **Container** — DI容器
- **Provider** — 对象提供者
- **Factory** — 每次请求创建新实例
- **Singleton** — 全局单例
- **Configuration** — 配置提供者

### 4.3 基本使用
`python
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[__name__]
    )

    # 配置
    config = providers.Configuration()

    # 数据库
    database = providers.Singleton(
        PostgresDatabase,
        url=config.db.url,
    )

    # 缓存
    cache = providers.Singleton(
        RedisCache,
        host=config.redis.host,
        port=config.redis.port,
    )

    # 服务（自动注入依赖）
    user_service = providers.Factory(
        UserService,
        db=database,
        cache=cache,
    )

# 在FastAPI中使用
@inject
def get_user_service(
    user_service: UserService = Provide[Container.user_service],
) -> UserService:
    return user_service
`

### 4.4 配置驱动
`python
import yaml

# config.yml
# db:
#   url: postgresql://localhost/mydb
# redis:
#   host: localhost
#   port: 6379

container = Container()
with open("config.yml") as f:
    config = yaml.safe_load(f)
container.config.from_dict(config)
`

---

## 第五部分：工厂模式与DI

### 5.1 简单工厂
`python
class PaymentProcessorFactory:
    _processors: dict[str, type] = {
        "credit_card": CreditCardProcessor,
        "paypal": PayPalProcessor,
        "alipay": AlipayProcessor,
    }

    @classmethod
    def create(cls, processor_type: str, **kwargs):
        processor_cls = cls._processors.get(processor_type)
        if not processor_cls:
            raise ValueError(f"Unknown processor: {processor_type}")
        return processor_cls(**kwargs)
`

### 5.2 注册表工厂
`python
class ServiceRegistry:
    _services: dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(factory_cls):
            cls._services[name] = factory_cls
            return factory_cls
        return decorator

    @classmethod
    def create(cls, name: str, **kwargs):
        return cls._services[name](**kwargs)

@ServiceRegistry.register("notification")
class EmailNotification:
    def __init__(self, smtp_host: str): ...

@ServiceRegistry.register("sms_notification")
class SMSNotification:
    def __init__(self, api_key: str): ...
`

---

## 第六部分：DI在实际项目中的应用

### 6.1 FastAPI + DI
`python
from fastapi import FastAPI, Depends

app = FastAPI()

# 依赖
async def get_db():
    db = AsyncSession(engine)
    try:
        yield db
    finally:
        await db.close()

async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

# 路由注入
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repo),
):
    return await repo.find_by_id(user_id)
`

### 6.2 生命周期管理
`python
class AppContainer:
    def __init__(self, config: dict):
        self._config = config
        self._instances: dict = {}

    async def startup(self):
        """应用启动时初始化"""
        self._instances["db"] = await create_engine(self._config["db_url"])
        self._instances["cache"] = await create_redis(self._config["redis_url"])

    async def shutdown(self):
        """应用关闭时清理"""
        for instance in self._instances.values():
            if hasattr(instance, "close"):
                await instance.close()

    def get(self, name: str):
        return self._instances[name]
`

---

## 课堂练习

### 练习：手动DI容器
`python
# 实现一个支持bind、resolve、singleton的DI容器
# 要求：
# 1. bind注册工厂函数
# 2. resolve获取实例
# 3. singleton确保全局只有一个实例
# 4. 支持依赖自动解析（间接依赖）
`

---

## 本课总结

| 概念 | 说明 |
|------|------|
| DI | 把依赖从外部传入，而不是内部创建 |
| IoC | 控制权反转，从代码转移到容器 |
| 构造函数注入 | 最推荐的DI方式 |
| DI容器 | 管理对象生命周期和依赖关系 |
| dependency-injector | Python DI框架 |
| FastAPI Depends | Web框架的DI支持 |
