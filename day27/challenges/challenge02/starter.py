"""
Challenge 02: 天气查询工具 - WeatherQuery
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime


class WeatherQuery:
    """天气查询工具"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.history = []
    
    def current(self, city: str, units: str = "metric") -> Dict:
        """获取当前天气"""
        # TODO: 实现
        pass
    
    def forecast(self, city: str, days: int = 5) -> List[Dict]:
        """获取天气预报"""
        # TODO: 实现
        pass
    
    def format_current(self, data: Dict) -> str:
        """格式化当前天气"""
        # TODO: 返回可读格式
        pass
    
    def get_history(self) -> List[Dict]:
        """获取查询历史"""
        return self.history


if __name__ == "__main__":
    # 注意：需要有效的 API Key
    weather = WeatherQuery("your_api_key")
    # current = weather.current("Beijing")
    # print(weather.format_current(current))
