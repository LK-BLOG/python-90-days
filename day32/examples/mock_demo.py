"""Mock 和 patch 演示"""

from unittest.mock import Mock, patch, AsyncMock
import asyncio


class WeatherAPI:
    def get_temperature(self, city: str) -> dict:
        # 真实实现会调用网络
        import requests
        resp = requests.get(f"https://api.weather.com/{city}")
        return resp.json()


class UserService:
    def __init__(self, db, mailer):
        self.db = db
        self.mailer = mailer

    def register(self, email: str, name: str) -> bool:
        if self.db.find_user(email):
            return False
        self.db.save_user(email, name)
        self.mailer.send_welcome(email, name)
        return True


class FakeDatabase:
    def __init__(self):
        self._users = {}

    def find_user(self, email):
        return self._users.get(email)

    def save_user(self, email, name):
        self._users[email] = {"name": name}


class SpyMailer:
    def __init__(self):
        self.sent = []

    def send_welcome(self, email, name):
        self.sent.append({"to": email, "name": name})


# 测试: patch 外部 API
@patch("__main__.WeatherAPI.get_temperature")
def test_weather_mock(mock_get):
    mock_get.return_value = {"temp": 25, "city": "Beijing"}
    api = WeatherAPI()
    result = api.get_temperature("Beijing")
    assert result["temp"] == 25
    mock_get.assert_called_once_with("Beijing")


# 测试: 使用 Fake 实现
def test_register_success():
    db = FakeDatabase()
    mailer = SpyMailer()
    service = UserService(db, mailer)

    result = service.register("alice@test.com", "Alice")
    assert result is True
    assert db.find_user("alice@test.com") is not None
    assert len(mailer.sent) == 1


def test_register_duplicate():
    db = FakeDatabase()
    db.save_user("alice@test.com", "Alice")
    mailer = SpyMailer()
    service = UserService(db, mailer)

    result = service.register("alice@test.com", "Bob")
    assert result is False
    assert len(mailer.sent) == 0


if __name__ == "__main__":
    print("Mock demo - run with pytest: pytest mock_demo.py -v")
