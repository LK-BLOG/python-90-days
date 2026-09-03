"""示例3：Cookie 和 Session"""
import urllib.request
import http.cookiejar
import json

def cookie_basic():
    """基础 Cookie 使用"""
    # 创建 Cookie 处理器
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar)
    )
    
    # 设置 Cookie
    response = opener.open("https://httpbin.org/cookies/set?token=abc123&user=test")
    
    # 获取 Cookie
    print("已设置的 Cookie:")
    for cookie in cookie_jar:
        print(f"  {cookie.name}: {cookie.value}")
    
    # 发送 Cookie
    response = opener.open("https://httpbin.org/cookies")
    result = json.loads(response.read())
    print("\n服务器收到的 Cookie:")
    print(json.dumps(result["cookies"], indent=2))

class Session:
    """简易 Session 实现"""
    
    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.headers = {"User-Agent": "MyApp/1.0"}
    
    def get(self, url):
        req = urllib.request.Request(url, headers=self.headers)
        response = self.opener.open(req)
        return json.loads(response.read())
    
    def post(self, url, data=None):
        if data:
            data = json.dumps(data).encode("utf-8")
            self.headers["Content-Type"] = "application/json"
        
        req = urllib.request.Request(url, data=data, headers=self.headers)
        response = self.opener.open(req)
        return json.loads(response.read())
    
    def cookies(self):
        return {c.name: c.value for c in self.cookie_jar}

def session_example():
    """Session 使用示例"""
    session = Session()
    
    # 登录（设置 Cookie）
    session.get("https://httpbin.org/cookies/set?session_id=xyz789")
    print(f"Session Cookies: {session.cookies()}")
    
    # 后续请求自动携带 Cookie
    result = session.get("https://httpbin.org/cookies")
    print(f"服务器收到: {result['cookies']}")

if __name__ == "__main__":
    print("=== Cookie 基础 ===")
    cookie_basic()
    
    print("\n=== Session 示例 ===")
    session_example()
