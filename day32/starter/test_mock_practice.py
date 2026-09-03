"""Challenge 2: Mock 和 patch - 骨架代码"""

from unittest.mock import Mock, patch, AsyncMock
import json


class FileService:
    \"\"\"文件服务 - TODO: 实现\"\"\"

    def __init__(self, fs_adapter):
        self.fs = fs_adapter

    def read_config(self, path: str) -> dict:
        \"\"\"读取配置文件 - TODO: 实现\"\"\"
        # TODO: 使用 fs_adapter 读取文件并解析 JSON
        pass

    def save_data(self, path: str, data: dict) -> bool:
        \"\"\"保存数据 - TODO: 实现\"\"\"
        pass


class EmailNotifier:
    def __init__(self, smtp_client):
        self.smtp = smtp_client

    def notify(self, to: str, subject: str, body: str) -> bool:
        \"\"\"发送通知 - TODO: 实现\"\"\"
        # TODO: 使用 smtp_client 发送邮件
        pass


# === TODO: 编写以下测试 ===

# 1. 用 Mock 测试 FileService.read_config
#    - mock fs_adapter 的 read 方法
#    - 验证返回了正确的 dict

# 2. patch 外部依赖测试 EmailNotifier
#    - 验证 smtp.send 被正确调用

# 3. 创建一个 FakeFileAdapter 类
#    - 模拟文件读写行为
#    - 不依赖真实文件系统

# 4. 测试异常情况
#    - 文件不存在
#    - JSON 格式错误
#    - SMTP 发送失败


if __name__ == "__main__":
    print("Run with: pytest test_mock_practice.py -v")
