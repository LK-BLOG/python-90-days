\"\"\"Day 48: 配置管理测试\"\"\"

import os
import pytest


def test_settings_defaults():
    from pydantic_settings import BaseSettings

    class TestSettings(BaseSettings):
        name: str = \"default\"
        port: int = 8000
        debug: bool = False

    s = TestSettings()
    assert s.name == \"default\"
    assert s.port == 8000
    assert s.debug is False


def test_settings_from_env():
    os.environ[\"TEST_NAME\"] = \"env-value\"
    os.environ[\"TEST_PORT\"] = \"3000\"

    from pydantic_settings import BaseSettings

    class TestSettings(BaseSettings):
        model_config = {\"env_prefix\": \"TEST_\"}
        name: str = \"default\"
        port: int = 8000

    s = TestSettings()
    assert s.name == \"env-value\"
    assert s.port == 3000

    del os.environ[\"TEST_NAME\"]
    del os.environ[\"TEST_PORT\"]


def test_settings_validation():
    from pydantic_settings import BaseSettings
    from pydantic import Field, ValidationError

    class ValidatedSettings(BaseSettings):
        port: int = Field(default=8000, ge=1, le=65535)

    s = ValidatedSettings(port=80)
    assert s.port == 80

    with pytest.raises(ValidationError):
        ValidatedSettings(port=99999)


def test_config_manager():
    from hot_reload import ConfigManager
    import tempfile, json, os

    path = tempfile.mktemp(suffix=\".json\")
    with open(path, \"w\") as f:
        json.dump({\"key\": \"value1\"}, f)

    mgr = ConfigManager()
    mgr.load(path)
    assert mgr.get(\"key\") == \"value1\"

    mgr.set(\"key\", \"value2\")
    assert mgr.get(\"key\") == \"value2\"

    os.unlink(path)
