# Day 26 课程：HTTP 协议

## 模块一：HTTP 协议基础

### 1.1 HTTP 是什么

HTTP（超文本传输协议）是客户端和服务器之间的通信协议。

```
客户端 (浏览器/Python)  ←→  服务器 (网站/API)
     请求 (Request)          响应 (Response)
```

### 1.2 请求方法

| 方法 | 用途 | 请求体 | 安全性 |
|------|------|--------|--------|
| GET | 获取资源 | 无 | 安全 |
| POST | 创建资源 | 有 | 不安全 |
| PUT | 更新资源（全量） | 有 | 不安全 |
| PATCH | 部分更新 | 有 | 不安全 |
| DELETE | 删除资源 | 可有 | 不安全 |
| HEAD | 获取响应头 | 无 | 安全 |
| OPTIONS | 获取支持的方法 | 无 | 安全 |

### 1.3 状态码

```
1xx：信息性
  100 Continue
  101 Switching Protocols

2xx：成功
  200 OK                    # 请求成功
  201 Created               # 资源创建成功
  204 No Content            # 成功，无内容

3xx：重定向
  301 Moved Permanently     # 永久重定向
  302 Found                 # 临时重定向
  304 Not Modified          # 资源未修改（缓存）

4xx：客户端错误
  400 Bad Request           # 请求格式错误
  401 Unauthorized          # 未认证
  403 Forbidden             # 无权限
  404 Not Found             # 资源不存在
  405 Method Not Allowed    # 方法不允许
  429 Too Many Requests     # 请求过多

5xx：服务器错误
  500 Internal Server Error # 服务器内部错误
  502 Bad Gateway           # 网关错误
  503 Service Unavailable   # 服务不可用
```

### 1.4 Headers（请求/响应头）

```
# 请求头
User-Agent: Mozilla/5.0...       # 客户端信息
Accept: application/json         # 接受的响应格式
Content-Type: application/json   # 请求体格式
Authorization: Bearer xxx        # 认证信息
Cookie: session=abc123           # Cookie
Host: example.com                # 目标主机
Accept-Encoding: gzip            # 接受的编码

# 响应头
Content-Type: text/html          # 响应体格式
Content-Length: 1234              # 响应体长度
Set-Cookie: session=abc123       # 设置 Cookie
Cache-Control: max-age=3600      # 缓存控制
Location: /new-url               # 重定向地址
```

### 1.5 请求/响应体

```
# 请求体（POST/PUT）
Content-Type: application/json
{
    "name": "张三",
    "email": "zhangsan@example.com"
}

# 响应体
Content-Type: application/json
{
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com"
}
```

---

## 模块二：使用 urllib/http.request

### 2.1 基础 GET 请求

```python
import urllib.request
import urllib.parse
import json

# 简单 GET 请求
response = urllib.request.urlopen("https://api.github.com/users/python")
data = json.loads(response.read())
print(data["login"])

# 带参数的 GET 请求
params = urllib.parse.urlencode({
    "q": "python",
    "sort": "stars",
    "per_page": 10
})
url = f"https://api.github.com/search/repositories?{params}"
response = urllib.request.urlopen(url)
data = json.loads(response.read())
print(f"找到 {data['total_count']} 个仓库")
```

### 2.2 POST 请求

```python
import urllib.request
import urllib.parse
import json

# POST 表单数据
data = urllib.parse.urlencode({
    "username": "test",
    "password": "123456"
}).encode("utf-8")

req = urllib.request.Request(
    "https://httpbin.org/post",
    data=data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read())
    print(result)
```

### 2.3 JSON 请求

```python
import urllib.request
import json

# JSON POST 请求
data = json.dumps({
    "name": "张三",
    "email": "zhangsan@example.com"
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
    print(result)
```

### 2.4 自定义 Headers

```python
import urllib.request

req = urllib.request.Request(
    "https://api.github.com/user",
    headers={
        "User-Agent": "MyApp/1.0",
        "Authorization": "Bearer YOUR_TOKEN",
        "Accept": "application/vnd.github.v3+json"
    }
)

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
```

### 2.5 处理错误

```python
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen("https://api.github.com/nonexistent")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
    print(f"原因: {e.reason}")
    print(f"响应头: {e.headers}")
    print(f"响应体: {e.read().decode()}")
except urllib.error.URLError as e:
    print(f"URL 错误: {e.reason}")
except Exception as e:
    print(f"其他错误: {e}")
```

### 2.6 使用 http.client（更底层）

```python
import http.client
import json

# 创建连接
conn = http.client.HTTPSConnection("api.github.com")

# 发送请求
conn.request("GET", "/users/python", headers={
    "User-Agent": "MyApp/1.0"
})

# 获取响应
response = conn.getresponse()
print(f"状态码: {response.status}")
print(f"响应头: {response.getheaders()}")

data = json.loads(response.read())
print(data["login"])

conn.close()
```

---

## 模块三：Cookie 和 Session

### 3.1 Cookie 基础

```python
import urllib.request
import http.cookiejar

# 创建 Cookie 处理器
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar)
)

# 请求会自动处理 Cookie
response = opener.open("https://httpbin.org/cookies/set?name=value")
response = opener.open("https://httpbin.org/cookies")

# 查看 Cookie
for cookie in cookie_jar:
    print(f"{cookie.name}: {cookie.value}")
```

### 3.2 保存/加载 Cookie

```python
import http.cookiejar

# 保存 Cookie 到文件
cookie_jar = http.cookiejar.MozillaCookieJar("cookies.txt")
# ... 发送请求 ...
cookie_jar.save()

# 加载 Cookie
cookie_jar = http.cookiejar.MozillaCookieJar("cookies.txt")
cookie_jar.load()
```

### 3.3 Session 模拟

```python
import urllib.request
import http.cookiejar
import json

class Session:
    """模拟 Session"""
    
    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.headers = {
            "User-Agent": "MyApp/1.0"
        }
    
    def get(self, url, **kwargs):
        """GET 请求"""
        req = urllib.request.Request(url, headers=self.headers)
        response = self.opener.open(req)
        return json.loads(response.read())
    
    def post(self, url, data=None, **kwargs):
        """POST 请求"""
        if data:
            data = json.dumps(data).encode("utf-8")
            self.headers["Content-Type"] = "application/json"
        
        req = urllib.request.Request(url, data=data, headers=self.headers)
        response = self.opener.open(req)
        return json.loads(response.read())

# 使用 Session
session = Session()
session.get("https://httpbin.org/cookies/set?session=abc123")
cookies = session.get("https://httpbin.org/cookies")
print(cookies)  # {"cookies": {"session": "abc123"}}
```

---

## 模块四：认证

### 4.1 Basic 认证

```python
import urllib.request
import base64

# 基础认证
username = "admin"
password = "secret"
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

req = urllib.request.Request(
    "https://httpbin.org/basic-auth/admin/secret",
    headers={
        "Authorization": f"Basic {credentials}"
    }
)

response = urllib.request.urlopen(req)
print(json.loads(response.read()))
```

### 4.2 Bearer Token 认证

```python
import urllib.request

token = "your_jwt_token_here"

req = urllib.request.Request(
    "https://api.github.com/user",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
)

response = urllib.request.urlopen(req)
print(json.loads(response.read()))
```

---

## 模块五：SSL/TLS 基础

### 5.1 SSL 验证

```python
import urllib.request
import ssl

# 默认 SSL 验证（推荐）
response = urllib.request.urlopen("https://api.github.com")

# 禁用 SSL 验证（不推荐，仅测试用）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

response = urllib.request.urlopen("https://self-signed.example.com", context=ctx)
```

---

## 模块六：实际应用

### 6.1 下载文件

```python
import urllib.request
import os

def download_file(url, save_path):
    """下载文件"""
    print(f"下载: {url}")
    
    def report(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = downloaded / total_size * 100
            print(f"\r进度: {percent:.1f}%", end="")
    
    urllib.request.urlretrieve(url, save_path, reporthook=report)
    print(f"\n保存到: {save_path}")

# 使用
download_file(
    "https://speed.hetzner.de/100MB.bin",
    "test_download.bin"
)
```

### 6.2 超时处理

```python
import urllib.request
import socket

# 设置全局超时
socket.setdefaulttimeout(30)

# 设置单个请求超时
try:
    response = urllib.request.urlopen(
        "https://api.github.com",
        timeout=10  # 10秒超时
    )
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print("请求超时")
```

---

## 常见错误汇总

| 错误 | 原因 | 解决 |
|------|------|------|
| HTTPError 400 | 请求格式错误 | 检查请求体和 Headers |
| HTTPError 401 | 未认证 | 添加认证信息 |
| HTTPError 403 | 无权限 | 检查权限配置 |
| HTTPError 404 | 资源不存在 | 检查 URL |
| URLError | 网络错误 | 检查网络连接 |
| SSL 错误 | 证书问题 | 配置 SSL 上下文 |
| TimeoutError | 请求超时 | 增加超时时间 |
