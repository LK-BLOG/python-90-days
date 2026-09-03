\"\"\"Pydantic Settings完整示例\"\"\"

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional


class AppSettings(BaseSettings):
    \"\"\"应用配置 — 从环境变量和.env文件读取\"\"\"

    # 基础配置
    app_name: str = \"MyApp\"
    app_version: str = \"1.0.0\"
    debug: bool = False
    log_level: str = \"INFO\"

    # 服务器
    host: str = \"0.0.0.0\"
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=1, ge=1)

    # 数据库
    database_url: str = \"sqlite:///app.db\"
    db_pool_size: int = Field(default=5, ge=1, le=100)

    # Redis
    redis_url: str = \"redis://localhost:6379\"

    # 安全
    secret_key: str = \"change-me-in-production\"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = [\"http://localhost:3000\"]

    model_config = {
        \"env_file\": \".env\",
        \"env_file_encoding\": \"utf-8\",
        \"env_prefix\": \"APP_\",
        \"case_sensitive\": False,
    }

    @field_validator(\"log_level\")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = {\"DEBUG\", \"INFO\", \"WARNING\", \"ERROR\", \"CRITICAL\"}
        if v.upper() not in valid:
            raise ValueError(f\"Invalid log level: {v}\")
        return v.upper()

    @field_validator(\"database_url\")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        valid_prefixes = (\"sqlite://\", \"postgresql://\", \"mysql://\")
        if not v.startswith(valid_prefixes):
            raise ValueError(f\"Invalid DB URL prefix: {v}\")
        return v


# 模拟环境变量
if __name__ == \"__main__\":
    import os
    os.environ[\"APP_DEBUG\"] = \"true\"
    os.environ[\"APP_DATABASE_URL\"] = \"postgresql://localhost/testdb\"
    os.environ[\"APP_SECRET_KEY\"] = \"my-super-secret-key\"
    os.environ[\"APP_CORS_ORIGINS\"] = '[\"http://localhost:3000\", \"https://example.com\"]'

    settings = AppSettings()
    print(f\"App: {settings.app_name} v{settings.app_version}\")
    print(f\"Debug: {settings.debug}\")
    print(f\"DB: {settings.database_url}\")
    print(f\"Port: {settings.port}\")
    print(f\"CORS: {settings.cors_origins}\")
    print(f\"Secret: {settings.secret_key}\")
