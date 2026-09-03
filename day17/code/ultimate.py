from dataclasses import dataclass, field
import json

@dataclass
class ServerConfig:
    host: str = 'localhost'
    port: int = 8080
    timeout: int = 30

@dataclass
class DatabaseConfig:
    url: str = '文件存储:///db.文件存储3'
    pool_size: int = 5

@dataclass
class AppConfig:
    server: ServerConfig = field(default_factory=ServerConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    debug: bool = False

class ConfigManager:
    # TODO: load, save, override, merge
    pass
