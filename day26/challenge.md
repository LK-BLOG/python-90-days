# Day 26 挑战：HTTP 协议实战

## 挑战 1：HTTP 请求构造器
**难度：** ⭐⭐

编写一个 HTTP 请求构造器：
- 构建 GET/POST/PUT/DELETE 请求
- 支持自定义 Headers
- 支持查询参数
- 支持 JSON 和表单数据

## 挑战 2：响应解析器
**难度：** ⭐⭐

编写一个 HTTP 响应解析器：
- 解析状态码和原因短语
- 解析响应头
- 解析 JSON/HTML/文本响应
- 处理编码问题

## 挑战 3：Cookie 管理器
**难度：** ⭐⭐⭐

编写一个 Cookie 管理器：
- 从响应中提取 Cookie
- 在请求中添加 Cookie
- Cookie 持久化
- Cookie 过期处理

## 挑战 4：认证管理器
**难度：** ⭐⭐⭐

编写一个认证管理器：
- Basic 认证
- Bearer Token 认证
- API Key 认证
- Session 持久化（本地存储Cookie/Session状态）

## 挑战 5：HTTP 客户端
**难度：** ⭐⭐⭐⭐

编写一个简单的 HTTP 客户端：
- 支持所有 HTTP 方法
- 支持 Headers 管理
- 支持 Cookie/Session
- 支持认证
- 支持超时和重试

## 🏆 Boss 挑战：完整 HTTP 客户端库
**难度：** ⭐⭐⭐⭐⭐

编写一个完整的 HTTP 客户端库（类似 requests 的简化版）：
- 支持所有 HTTP 方法
- 完整的 Headers/Cookie 管理
- 多种认证方式
- SSL/TLS 支持
- 代理支持
- 超时和重试机制
- 文件上传/下载
- Session 管理

