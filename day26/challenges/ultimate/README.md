# MiniRequests — 简化版 requests 库

> Day 26 终极挑战 | 难度：★★★★★

## 目标

使用 Python 标准库（`urllib`、`http.cookiejar`、`ssl` 等）实现一个简化版的 `requests` 库，理解 HTTP 请求的底层机制。

## 功能要求

- **Response 对象**：封装状态码、响应头、响应体，提供 `.json()`、`.text`、`.ok`、`.raise_for_status()` 等属性和方法
- **HTTPError 异常类**：HTTP 错误时抛出自定义异常，携带状态码和响应对象
- **Session 会话**：支持 Cookie 持久化、SSL 上下文配置、自定义请求头
- **请求方法**：实现 GET / POST / PUT / PATCH / DELETE / HEAD / OPTIONS
- **请求准备**：URL 参数拼接、请求体编码（form-data / JSON）、请求头合并
- **重试机制**：可配置最大重试次数和重试间隔
- **模块级快捷函数**：`get()` 和 `post()` 无需手动管理 Session

## 验收标准

- [ ] `get("https://httpbin.org/get")` 返回正确状态码和 JSON 数据
- [ ] `Session` 能自动管理 Cookie（`/cookies/set` → `/cookies` 验证）
- [ ] POST 请求支持 JSON body（`json_data` 参数）
- [ ] SSL 可配置关闭验证（`verify_ssl=False`）
- [ ] 请求失败时自动重试，且遵守 `max_retries` 限制
- [ ] `Response.raise_for_status()` 在 4xx/5xx 时抛出 `HTTPError`
- [ ] 所有 TODO 注释处均已实现
