"""示例3：异常处理和重试"""
import requests
import time
from requests.exceptions import (
    RequestException, HTTPError, ConnectionError, Timeout
)

def simple_request():
    """简单请求"""
    try:
        response = requests.get("https://httpbin.org/status/200", timeout=10)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(f"HTTP 错误: {e.response.status_code}")
    except ConnectionError:
        print("连接错误")
    except Timeout:
        print("请求超时")
    except RequestException as e:
        print(f"请求异常: {e}")

def request_with_retry(url, max_retries=3, delay=1, backoff=2):
    """带重试的请求"""
    for attempt in range(max_retries):
        try:
            print(f"尝试 {attempt + 1}/{max_retries}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay * (backoff ** attempt)
            print(f"失败，{wait_time}秒后重试...")
            time.sleep(wait_time)

def using_retry_adapter():
    """使用 urllib3 重试适配器"""
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    response = session.get("https://httpbin.org/get")
    return response.json()

if __name__ == "__main__":
    print("=== 简单请求 ===")
    simple_request()
    
    print("\n=== 带重试的请求 ===")
    try:
        result = request_with_retry("https://httpbin.org/get")
        print(f"成功: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
    
    print("\n=== 使用重试适配器 ===")
    try:
        result = using_retry_adapter()
        print(f"成功: {result}")
    except Exception as e:
        print(f"失败: {e}")
