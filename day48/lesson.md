# Day 48 课程：配置管理

## 第一部分：配置管理基础

### 1.1 为什么需要配置管理
- 不同环境（dev/staging/prod）不同配置
- 敏感信息（密码/API Key）不能硬编码
- 配置变更不需要改代码重部署
- 配置验证防止错误配置上线

### 1.2 配置来源优先级（从低到高）
1. 硬编码默认值
2. 配置文件（config.yml/config.json）
3. 环境变量
4. 命令行参数
5. 运行时覆盖（热更新）

---

## 第二部分：python-dotenv

### 2.1 基本使用
`ash
pip install python-dotenv
`

`python
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()  # 自动查找.env

# 或指定路径
load_dotenv(".env.production")

# 读取
db_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
api_key = os.getenv("API_KEY", "")
`

### 2.2 .env文件结构
`ash
# .env（开发环境）
DATABASE_URL=sqlite:///dev.db
DEBUG=true
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key

# .env.production（生产环境）
DATABASE_URL=postgresql://prod-host/mydb
DEBUG=false
REDIS_URL=redis://prod-redis:6379/0
SECRET_KEY=super-secure-production-key
`

---

## 第三部分：Pydantic Settings

### 3.1 安装
`ash
pip install pydantic-settings
`

### 3.2 基本使用
`python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # 自动从环境变量读取
    database_url: str = "sqlite:///default.db"
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    secret_key: str = "change-me"
    api_key: str = ""
    max_connections: int = 10

    # 嵌套配置
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_prefix": "APP_",  # 环境变量前缀: APP_DATABASE_URL
        "case_sensitive": False,
    }

# 使用
settings = Settings()
print(settings.database_url)
print(settings.debug)
`

### 3.3 验证
`python
from pydantic import Field, field_validator

class Settings(BaseSettings):
    database_url: str = Field(..., description="数据库连接URL")
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = Field(default="INFO")

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        if not v.startswith(("sqlite://", "postgresql://", "mysql://")):
            raise ValueError(f"Invalid database URL: {v}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid:
            raise ValueError(f"Invalid log level: {v}, must be one of {valid}")
        return v.upper()
`

---

## 第四部分：多环境配置

### 4.1 目录结构
`
config/
├── settings.py       # 基础配置类
├── settings_dev.py   # 开发环境
├── settings_prod.py  # 生产环境
├── settings_test.py  # 测试环境
└── __init__.py       # 根据环境选择
`

### 4.2 环境选择
`python
import os

def get_settings() -> BaseSettings:
    env = os.getenv("APP_ENV", "development")

    if env == "production":
        from .settings_prod import ProdSettings
        return ProdSettings()
    elif env == "testing":
        from .settings_test import TestSettings
        return TestSettings()
    else:
        from .settings_dev import DevSettings
        return DevSettings()

settings = get_settings()
`

### 4.3 环境差异
`python
# Dev
class DevSettings(BaseSettings):
    database_url: str = "sqlite:///dev.db"
    debug: bool = True
    log_level: str = "DEBUG"
    cors_origins: list[str] = ["http://localhost:3000"]

# Production
class ProdSettings(BaseSettings):
    database_url: str  # 必须从环境变量读取
    debug: bool = False
    log_level: str = "WARNING"
    cors_origins: list[str] = []  # 从环境变量读取
    model_config = {"env_file": ".env.production"}
`

---

## 第五部分：配置热更新

### 5.1 文件监控
`python
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def on_modified(self, event):
        if event.src_path.endswith(('.yml', '.yaml', '.json')):
            print(f"Config file changed: {event.src_path}")
            self.config_manager.reload()

class ConfigManager:
    def __init__(self):
        self._settings: Settings | None = None
        self._callbacks: list[callable] = []

    def load(self) -> Settings:
        self._settings = Settings()
        return self._settings

    def reload(self) -> Settings:
        self._settings = Settings()
        for cb in self._callbacks:
            cb(self._settings)
        return self._settings

    def on_change(self, callback: callable):
        self._callbacks.append(callback)
`

### 5.2 远程配置
`python
import httpx

class RemoteConfigLoader:
    def __init__(self, config_server_url: str):
        self.url = config_server_url

    async def fetch(self, key: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f\"{self.url}/config/{key}\")
            return resp.json()
`

---

## 课堂练习

### 练习：完整配置系统
`python
# 实现一个支持以下功能的配置系统：
# 1. 从.env文件读取
# 2. 支持环境变量覆盖
# 3. Pydantic验证
# 4. 多环境切换
# 5. 配置缓存
`

---

## 本课总结

| 工具 | 用途 |
|------|------|
| python-dotenv | 加载.env文件 |
| pydantic-settings | 类型安全的配置 |
| os.getenv | 读取环境变量 |
| watchdog | 文件监控/热更新 |
| 多环境配置 | dev/staging/prod切换 |
