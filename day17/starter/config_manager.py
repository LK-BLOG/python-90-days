"""
Day 17 - dataclass
===============================
练习：用 dataclass 构建配置管理系统

要求：
- 使用 @dataclass / @dataclass(frozen=True) 等特性
- 字段验证、默认值、post_init
- 序列化/反序列化（to_dict / from_dict）
- 配置管理器的嵌套与合并

运行本文件测试你的实现是否正确。
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import json


@dataclass
class DatabaseConfig:
    """数据库配置

    字段:
        host:     主机地址，默认 'localhost'
        port:     端口号，默认 3306
        username: 用户名
        password: 密码，默认空字符串
        db_name:  数据库名

    TODO:
        1. 实现 __post_init__ 验证 port 范围 (1-65535)
        2. 实现 connection_string 属性 (property)
    """
    host: str = 'localhost'
    port: int = 3306
    username: str = ''
    password: str = ''
    db_name: str = ''

    # TODO: __post_init__ 验证端口范围

    @property
    def connection_string(self) -> str:
        """返回数据库连接字符串"""
        # TODO: 格式 mysql+pymysql://user:pass@host:port/db
        pass


@dataclass
class AppConfig:
    """应用配置

    字段:
        app_name:    应用名称
        debug:       调试模式，默认 False
        log_level:   日志级别，默认 'INFO'
        database:    数据库配置
        max_retries: 最大重试次数，默认 3

    TODO:
        1. database 字段使用 field(default_factory=DatabaseConfig)
        2. 实现 validate() 检查必填字段
        3. 实现 to_dict() / from_dict() 序列化
        4. 实现 merge(other: AppConfig) 合并配置（other 覆盖 self）
    """
    app_name: str = ''
    debug: bool = False
    log_level: str = 'INFO'
    database: DatabaseConfig = None     # TODO: 改用 field(default_factory=...)
    max_retries: int = 3

    def validate(self) -> bool:
        """验证配置合法性

        TODO:
            - app_name 不能为空
            - log_level 必须是 DEBUG/INFO/WARNING/ERROR/CRITICAL 之一
            - 验证失败抛出 ValueError
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典（包含嵌套的 DatabaseConfig）"""
        # TODO: 用 asdict 或手动转换
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """从字典反序列化"""
        # TODO: 处理嵌套的 database 字段
        pass

    def to_json(self, indent=2) -> str:
        """序列化为 JSON 字符串"""
        # TODO: json.dumps(self.to_dict(), ...)
        pass

    @classmethod
    def from_json(cls, json_str: str):
        """从 JSON 字符串反序列化"""
        # TODO: json.loads -> from_dict
        pass

    def merge(self, other: 'AppConfig') -> 'AppConfig':
        """合并两个配置，other 的值覆盖 self

        TODO: 实现深度合并
        """
        pass


# ==================== 测试 ====================
if __name__ == '__main__':
    print('=' * 50)
    print('Day 17 练习: dataclass 配置管理')
    print('=' * 50)

    db = DatabaseConfig(host='127.0.0.1', port=3306, username='root', db_name='myapp')
    print(f'DB: {db}')
    print(f'连接字符串: {db.connection_string}')

    config = AppConfig(
        app_name='MyApp',
        debug=True,
        database=db,
    )
    print(f'Config: {config}')

    d = config.to_dict()
    print(f'to_dict: {d}')

    config2 = AppConfig.from_dict(d)
    print(f'from_dict: {config2}')

    json_str = config.to_json()
    print(f'JSON:\n{json_str}')

    config3 = AppConfig.from_json(json_str)
    assert config3.app_name == 'MyApp'
    assert config3.debug == True

    # 端口范围验证
    try:
        bad_db = DatabaseConfig(port=99999)
        print('ERROR: 应该抛出 ValueError')
    except ValueError as e:
        print(f'验证捕获: {e}')

    print('OK -- 所有测试通过!')
