# Day 27 - Challenge 2: 天气查询工具
# 难度: ⭐⭐
# 使用 OpenWeatherMap API 查询天气、5天预报、图标下载、历史记录

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen


@dataclass
class WeatherInfo:
    """天气信息"""
    city: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    icon: str
    wind_speed: float
    timestamp: float


class WeatherClient:
    """天气查询客户端

    使用 OpenWeatherMap API 查询天气信息。
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        """初始化

        Args:
            api_key: OpenWeatherMap API Key
        """
        self.api_key = api_key
        # TODO: 初始化历史记录存储
        self._history: list[dict] = []
        self._history_file = Path("weather_history.json")

    def get_current(self, city: str, units: str = "metric") -> WeatherInfo:
        """查询当前天气

        Args:
            city: 城市名
            units: 单位（metric/imperial）

        Returns:
            WeatherInfo 对象
        """
        # TODO: GET /weather?q={city}&appid={key}&units={units}
        # TODO: 解析响应为 WeatherInfo
        ...

    def get_forecast(self, city: str, days: int = 5) -> list[dict]:
        """查询 5 天预报

        Args:
            city: 城市名
            days: 预报天数

        Returns:
            预报数据列表
        """
        # TODO: GET /forecast?q={city}
        # TODO: 按天聚合数据
        ...

    def download_icon(self, icon_code: str, save_dir: str = "icons") -> Path:
        """下载天气图标

        Args:
            icon_code: 图标代码（如 10d）
            save_dir: 保存目录

        Returns:
            图标文件路径
        """
        # TODO: 下载 https://openweathermap.org/img/wn/{icon_code}@2x.png
        ...

    def save_history(self) -> None:
        """保存查询历史到文件"""
        # TODO: 将 _history 序列化为 JSON
        ...

    def load_history(self) -> None:
        """从文件加载历史记录"""
        # TODO: 读取 JSON 文件
        ...

    def get_history(self, city: str = None) -> list[dict]:
        """获取历史查询记录

        Args:
            city: 过滤城市名，None 返回全部

        Returns:
            历史记录列表
        """
        # TODO: 按城市过滤历史记录
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    # 使用测试 API Key（实际使用需要注册）
    client = WeatherClient("demo_key")
    print("天气查询工具初始化完成")
    print("注意：需要有效的 OpenWeatherMap API Key 才能实际查询")
