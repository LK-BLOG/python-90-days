# Day 26 终极挑战：完整 HTTP 客户端库

## 项目名称：MiniRequests

## 背景
requests 库非常好用，但它是第三方库。现在要手写一个简化版。

## 目标
编写一个功能完整的 HTTP 客户端库，支持常用的 HTTP 操作。

## 功能要求

### 1. 基础请求
- GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS
- URL 构建和参数处理
- 请求体（JSON、表单、文件）

### 2. Headers 管理
- 默认 Headers
- 自定义 Headers
- Headers 合并

### 3. Cookie/Session
- Cookie 自动处理
- Session 管理
- Cookie 持久化

### 4. 认证
- Basic 认证
- Bearer Token
- API Key

### 5. 高级功能
- SSL/TLS 验证
- 代理支持
- 超时控制
- 重试机制
- 文件上传/下载
- 重定向控制

### 6. 响应处理
- 状态码检查
- 响应体解析（JSON、文本、二进制）
- 流式响应

## 输入
HTTP 请求参数

## 输出
HTTP 响应对象

## 限制
- 只使用标准库（urllib、http.client）
- 不能使用 requests 或 httpx
- 支持 Python 3.9+

## 示例
```python
from mini_requests import Session

# 基础 GET
response = session.get("https://api.github.com/users/python")
print(response.json())

# POST JSON
response = session.post(
    "https://httpbin.org/post",
    json={"name": "test"}
)

# 文件上传
response = session.post(
    "https://httpbin.org/post",
    files={"file": open("test.txt", "rb")}
)

# 认证
response = session.get(
    "https://api.github.com/user",
    auth=("username", "token")
)

# Session
with Session() as s:
    s.get("https://httpbin.org/cookies/set?token=abc123")
    response = s.get("https://httpbin.org/cookies")
    print(response.json())  # {"cookies": {"token": "abc123"}}
```

## 验收标准
- [ ] 支持所有 HTTP 方法
- [ ] 支持 JSON 请求/响应
- [ ] 支持 Cookie/Session
- [ ] 支持 Basic/Bearer 认证
- [ ] 支持文件上传
- [ ] 支持超时和重试
- [ ] 响应对象支持 json()、text、content 属性
- [ ] 错误处理完善

## 可选扩展
- 支持异步请求
- 支持 HTTP/2
- 支持 WebSocket
- 支持缓存
- 支持连接池
