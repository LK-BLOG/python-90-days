\"\"\"多环境配置切换\"\"\"

import os
from pydantic_settings import BaseSettings
from pydantic import Field


class BaseAppSettings(BaseSettings):
    app_name: str = \"MyApp\"
    log_level: str = \"INFO\"


class DevSettings(BaseAppSettings):
    debug: bool = True
    database_url: str = \"sqlite:///dev.db\"
    redis_url: str = \"redis://localhost:6379/0\"
    log_level: str = \"DEBUG\"
    cors_origins: list[str] = [\"http://localhost:3000\"]


class StagingSettings(BaseAppSettings):
    debug: bool = False
    database_url: str  # 必须设置
    redis_url: str     # 必须设置
    log_level: str = \"INFO\"
    cors_origins: list[str] = [\"https://staging.example.com\"]


class ProdSettings(BaseAppSettings):
    debug: bool = False
    database_url: str  # 必须设置
    redis_url: str     # 必须设置
    log_level: str = \"WARNING\"
    workers: int = Field(default=4, ge=1)
    cors_origins: list[str] = []  # 从环境变量读取


def get_settings() -> BaseAppSettings:
    env = os.getenv(\"APP_ENV\", \"development\").lower()

    settings_map = {
        \"development\": DevSettings,
        \"staging\": StagingSettings,
        \"production\": ProdSettings,
    }

    settings_cls = settings_map.get(env)
    if not settings_cls:
        raise ValueError(f\"Unknown environment: {env}\")
    return settings_cls()


if __name__ == \"__main__\":
    for env in [\"development\", \"staging\", \"production\"]:
        os.environ[\"APP_ENV\"] = env
        if env != \"development\":
            os.environ[\"DATABASE_URL\"] = f\"postgresql://{env}-host/mydb\"
            os.environ[\"REDIS_URL\"] = f\"redis://{env}-redis:6379\"
        try:
            s = get_settings()
            print(f\"{env}: debug={s.debug}, log={s.log_level}, db={s.database_url}\")
        except Exception as e:
            print(f\"{env}: Error - {e}\")
