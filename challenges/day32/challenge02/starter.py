# Challenge 02: Mock 和 patch
from unittest.mock import Mock, patch

class APIClient:
    def __init__(self, http):
        self.http = http
    def get_user(self, user_id: int) -> dict:
        # TODO: 使用 http.get 获取用户
        pass

# TODO: 用 patch 测试 get_user
# TODO: 创建 FakeHTTP 类
