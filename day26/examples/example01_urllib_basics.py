"""示例1：urllib 基础请求"""
import urllib.request
import urllib.parse
import json
import ssl

def basic_get():
    """基础 GET 请求"""
    url = "https://httpbin.org/get"
    
    response = urllib.request.urlopen(url)
    
    print(f"状态码: {response.status}")
    print(f"响应头: {dict(response.headers)}")
    
    data = json.loads(response.read())
    print(f"响应体: {json.dumps(data, indent=2)}")

def get_with_params():
    """带参数的 GET 请求"""
    params = urllib.parse.urlencode({
        "name": "张三",
        "age": 25,
        "city": "北京"
    })
    url = f"https://httpbin.org/get?{params}"
    
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    
    print("查询参数:")
    for key, value in data["args"].items():
        print(f"  {key}: {value}")

def get_with_headers():
    """带 Headers 的 GET 请求"""
    url = "https://httpbin.org/headers"
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
        "X-Custom-Header": "custom-value"
    })
    
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    
    print("请求头:")
    for key, value in data["headers"].items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print("=== 基础 GET ===")
    basic_get()
    
    print("\n=== 带参数 GET ===")
    get_with_params()
    
    print("\n=== 带 Headers ===")
    get_with_headers()
