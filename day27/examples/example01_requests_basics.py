"""示例1：requests 基础"""
import requests
import json

def basic_get():
    """基础 GET 请求"""
    response = requests.get("https://httpbin.org/get")
    
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"JSON: {json.dumps(response.json(), indent=2)}")

def get_with_params():
    """带参数的 GET"""
    params = {
        "name": "张三",
        "age": 25,
        "city": "北京"
    }
    response = requests.get("https://httpbin.org/get", params=params)
    
    print("查询参数:")
    for key, value in response.json()["args"].items():
        print(f"  {key}: {value}")

def post_json():
    """POST JSON 数据"""
    data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "skills": ["Python", "HTTP", "API"]
    }
    response = requests.post("https://httpbin.org/post", json=data)
    
    print("发送的 JSON:")
    print(json.dumps(response.json()["json"], indent=2, ensure_ascii=False))

def custom_headers():
    """自定义 Headers"""
    headers = {
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
        "X-Custom-Header": "custom-value"
    }
    response = requests.get("https://httpbin.org/headers", headers=headers)
    
    print("请求头:")
    for key, value in response.json()["headers"].items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print("=== 基础 GET ===")
    basic_get()
    
    print("\n=== 带参数 GET ===")
    get_with_params()
    
    print("\n=== POST JSON ===")
    post_json()
    
    print("\n=== 自定义 Headers ===")
    custom_headers()
