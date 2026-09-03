"""示例2：POST 请求和 JSON"""
import urllib.request
import json

def post_form():
    """POST 表单数据"""
    import urllib.parse
    
    data = urllib.parse.urlencode({
        "username": "testuser",
        "password": "testpass123"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://httpbin.org/post",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print("表单数据:")
        print(json.dumps(result["form"], indent=2))

def post_json():
    """POST JSON 数据"""
    data = json.dumps({
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25,
        "skills": ["Python", "HTTP", "API"]
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://httpbin.org/post",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print("JSON 数据:")
        print(json.dumps(json.loads(result["data"]), indent=2))

def put_request():
    """PUT 请求"""
    data = json.dumps({
        "id": 1,
        "name": "张三（已更新）"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://httpbin.org/put",
        data=data,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print("PUT 响应:")
        print(json.dumps(json.loads(result["data"]), indent=2))

def delete_request():
    """DELETE 请求"""
    req = urllib.request.Request(
        "https://httpbin.org/delete",
        method="DELETE"
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print("DELETE 响应:")
        print(f"方法: {result['method']}")

if __name__ == "__main__":
    print("=== POST 表单 ===")
    post_form()
    
    print("\n=== POST JSON ===")
    post_json()
    
    print("\n=== PUT ===")
    put_request()
    
    print("\n=== DELETE ===")
    delete_request()
