"""示例4：认证和错误处理"""
import urllib.request
import urllib.error
import base64
import json

def basic_auth():
    """Basic 认证"""
    # 凭证编码
    credentials = base64.b64encode(b"admin:password123").decode()
    
    req = urllib.request.Request(
        "https://httpbin.org/basic-auth/admin/password123",
        headers={"Authorization": f"Basic {credentials}"}
    )
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        print(f"认证成功: {data}")
    except urllib.error.HTTPError as e:
        print(f"认证失败: {e.code}")

def bearer_token():
    """Bearer Token 认证"""
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    
    req = urllib.request.Request(
        "https://httpbin.org/bearer",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        print(f"Token 认证: {data}")
    except urllib.error.HTTPError as e:
        print(f"Token 错误: {e.code}")

def error_handling():
    """错误处理示例"""
    # 测试不同的错误
    test_urls = [
        ("https://httpbin.org/status/200", "成功"),
        ("https://httpbin.org/status/404", "未找到"),
        ("https://httpbin.org/status/500", "服务器错误"),
        ("https://httpbin.org/status/401", "未认证"),
        ("https://httpbin.org/status/403", "无权限"),
    ]
    
    for url, desc in test_urls:
        try:
            response = urllib.request.urlopen(url)
            print(f"{desc}: {response.status}")
        except urllib.error.HTTPError as e:
            print(f"{desc}: HTTP 错误 {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"{desc}: URL 错误 - {e.reason}")

def download_with_retry():
    """带重试的下载"""
    import time
    
    url = "https://httpbin.org/delay/1"
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"尝试 {attempt + 1}/{max_retries}...")
            response = urllib.request.urlopen(url, timeout=5)
            data = json.loads(response.read())
            print(f"成功: {data}")
            return data
        except urllib.error.URLError as e:
            if "timed out" in str(e.reason):
                print(f"超时，{2 ** attempt}秒后重试...")
                time.sleep(2 ** attempt)
            else:
                raise
    
    raise Exception("重试次数已用完")

if __name__ == "__main__":
    print("=== Basic 认证 ===")
    basic_auth()
    
    print("\n=== Bearer Token ===")
    bearer_token()
    
    print("\n=== 错误处理 ===")
    error_handling()
    
    print("\n=== 重试机制 ===")
    try:
        download_with_retry()
    except Exception as e:
        print(f"最终失败: {e}")
