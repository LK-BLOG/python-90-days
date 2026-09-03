# Day 27 课程：API 实战

## 模块一：requests 库全面使用

### 1.1 安装和基础

```bash
pip install requests
```

```python
import requests

# GET 请求
response = requests.get("https://api.github.com/users/python")
print(response.status_code)  # 200
print(response.json())       # JSON 数据
print(response.text)         # 文本
print(response.content)      # 二进制
print(response.headers)      # 响应头
print(response.url)          # 请求 URL
print(response.elapsed)      # 耗时
```

### 1.2 Session

```python
import requests

# 使用 Session 保持 Cookie
with requests.Session() as s:
    # 登录
    s.post("https://example.com/login", data={
        "username": "user",
        "password": "pass"
    })
    
    # 后续请求自动携带 Cookie
    response = s.get("https://example.com/dashboard")
    print(response.status_code)
```

### 1.3 请求参数

```python
import requests

# 查询参数
params = {
    "q": "python",
    "sort": "stars",
    "per_page": 10
}
response = requests.get("https://api.github.com/search/repositories", params=params)
print(response.json()["total_count"])

# 表单数据
data = {
    "username": "test",
    "password": "123456"
}
response = requests.post("https://httpbin.org/post", data=data)

# JSON 数据
json_data = {
    "name": "张三",
    "email": "zhangsan@example.com"
}
response = requests.post("https://httpbin.org/post", json=json_data)
print(response.json()["json"])
```

### 1.4 自定义 Headers

```python
import requests

headers = {
    "User-Agent": "MyApp/1.0",
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/vnd.github.v3+json",
    "X-Custom-Header": "custom-value"
}

response = requests.get("https://api.github.com/user", headers=headers)
```

### 1.5 文件上传

```python
import requests

# 上传文件
files = {
    "file": ("test.txt", open("test.txt", "rb"), "text/plain")
}
response = requests.post("https://httpbin.org/post", files=files)
print(response.json()["files"])

# 上传多个文件
files = {
    "file1": open("file1.txt", "rb"),
    "file2": open("file2.txt", "rb")
}
response = requests.post("https://httpbin.org/post", files=files)
```

### 1.6 文件下载

```python
import requests

# 流式下载大文件
url = "https://speed.hetzner.de/100MB.bin"
response = requests.get(url, stream=True)

with open("download.bin", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# 进度条
import tqdm

total_size = int(response.headers.get("content-length", 0))
with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
    with open("download.bin", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
```

---

## 模块二：REST API 设计概念

### 2.1 RESTful URL 设计

```
GET    /api/users           # 获取用户列表
POST   /api/users           # 创建用户
GET    /api/users/1         # 获取单个用户
PUT    /api/users/1         # 更新用户（全量）
PATCH  /api/users/1         # 更新用户（部分）
DELETE /api/users/1         # 删除用户

# 嵌套资源
GET    /api/users/1/posts   # 获取用户的帖子
POST   /api/users/1/posts   # 为用户创建帖子
```

### 2.2 分页

```python
import requests

# 页码分页
response = requests.get("https://api.github.com/users", params={
    "page": 1,
    "per_page": 30
})

# Link 头分页
link_header = response.headers.get("Link", "")
# 解析下一页 URL

# Cursor 分页（某些 API）
response = requests.get("https://api.example.com/items", params={
    "cursor": "abc123",
    "limit": 30
})
```

### 2.3 认证方式

```python
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

# Basic 认证
response = requests.get(
    "https://api.github.com/user",
    auth=HTTPBasicAuth("username", "token")
)

# Bearer Token
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = requests.get("https://api.github.com/user", headers=headers)

# API Key（Header）
headers = {"X-API-Key": "your_api_key"}
response = requests.get("https://api.example.com/data", headers=headers)

# API Key（Query 参数）
params = {"api_key": "your_api_key"}
response = requests.get("https://api.example.com/data", params=params)
```

---

## 模块三：异常处理

### 3.1 requests 异常层次

```python
import requests
from requests.exceptions import (
    RequestException,      # 基类
    HTTPError,             # HTTP 错误
    ConnectionError,       # 连接错误
    Timeout,               # 超时
    URLRequired,           # URL 必需
    TooManyRedirects,      # 重定向过多
    MissingSchema,         # 缺少 URL schema
    InvalidSchema,         # 无效 schema
    InvalidURL,            # 无效 URL
    ChunkedEncodingError,  # 编码错误
    ContentDecodingError,  # 解码错误
)
```

### 3.2 异常处理

```python
import requests

try:
    response = requests.get("https://api.github.com/user", timeout=10)
    response.raise_for_status()  # 抛出 HTTPError
    data = response.json()
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.ConnectionError:
    print("连接错误")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")
```

---

## 模块四：重试机制

### 4.1 手动重试

```python
import requests
import time

def request_with_retry(url, max_retries=3, delay=1, backoff=2):
    """带重试的请求"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay * (backoff ** attempt)
            print(f"请求失败，{wait_time}秒后重试...")
            time.sleep(wait_time)

response = request_with_retry("https://api.github.com/users/python")
```

### 4.2 urllib3 重试

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 创建重试策略
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
)

# 创建 Session 并挂载适配器
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# 使用
response = session.get("https://api.github.com/users/python")
```

---

## 模块五：速率限制

### 5.1 简单限速

```python
import time
import requests
from functools import wraps

def rate_limiter(max_calls: int, period: float):
    """速率限制装饰器"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # 清除过期记录
            while calls and calls[0] <= now - period:
                calls.pop(0)
            
            # 检查是否超过限制
            if len(calls) >= max_calls:
                sleep_time = calls[0] + period - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
                calls.pop(0)
            
            calls.append(time.time())
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@rate_limiter(max_calls=10, period=60)  # 每分钟最多10次
def api_call():
    return requests.get("https://api.github.com/users/python")
```

---

## 模块六：API 封装最佳实践

### 6.1 封装 GitHub API 客户端

```python
import requests
from typing import Dict, List, Optional

class GitHubClient:
    """GitHub API 客户端"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PythonGitHubClient/1.0"
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    
    def _request(self, method: str, path: str, **kwargs) -> Dict:
        """发送请求"""
        url = f"{self.BASE_URL}{path}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_user(self, username: str) -> Dict:
        """获取用户信息"""
        return self._request("GET", f"/users/{username}")
    
    def get_repos(self, username: str, page: int = 1, per_page: int = 30) -> List[Dict]:
        """获取用户仓库"""
        return self._request("GET", f"/users/{username}/repos",
                            params={"page": page, "per_page": per_page})
    
    def search_repos(self, query: str, **params) -> Dict:
        """搜索仓库"""
        return self._request("GET", "/search/repositories",
                            params={"q": query, **params})

# 使用
client = GitHubClient(token="your_token")
user = client.get_user("octocat")
print(f"用户: {user['name']}")
repos = client.get_repos("octocat")
print(f"仓库数: {len(repos)}")
```

---

## 常见错误汇总

| 错误 | 原因 | 解决 |
|------|------|------|
| `ConnectionError` | 网络问题 | 检查网络、DNS |
| `Timeout` | 请求超时 | 增加 timeout、使用重试 |
| `HTTPError 401` | 认证失败 | 检查 Token/密码 |
| `HTTPError 403` | 无权限/限速 | 检查权限、等待限速恢复 |
| `HTTPError 404` | 资源不存在 | 检查 URL |
| `JSONDecodeError` | 响应不是 JSON | 检查 Content-Type |
