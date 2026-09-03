\"\"\"Day 48 Starter: 配置管理练习\"\"\"

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


# TODO: 实现AppSettings类
# 要求：
# 1. 至少6个配置项
# 2. 环境变量前缀APP_
# 3. 从.env文件读取
# 4. 包含验证器
# 5. 支持多环境切换

class AppSettings(BaseSettings):
    pass  # 实现这里...

# TODO: 实现get_settings函数
# 要求：根据APP_ENV返回对应配置

def get_settings():
    pass  # 实现这里...
