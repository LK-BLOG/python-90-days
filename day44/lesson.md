# Day 44 课程：安全基础

## 第一部分：常见漏洞

### 1.1 SQL 注入

`python
# 危险！不要这样做
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# 输入: ' OR '1'='1' --
# 变成: SELECT * FROM users WHERE name = '' OR '1'='1' --'

# 安全：参数化查询
# SQLAlchemy
user = session.query(User).filter(User.name == user_input).first()

# sqlite3
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# psycopg2
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
`

### 1.2 XSS（跨站脚本）

`python
# 危险：直接输出用户输入
# <script>document.cookie</script>

# 安全：转义输出
from markupsafe import escape
safe_output = escape(user_input)

# FastAPI 默认转义 JSON 响应
# 但返回 HTML 时需要手动转义
`

### 1.3 CSRF（跨站请求伪造）

`python
# 防护：CSRF Token
# 1. 服务器生成 token
# 2. 表单中嵌入 token
# 3. 提交时验证 token

from fastapi import Form

@app.post("/transfer")
async def transfer(amount: float, csrf_token: str = Form(...)):
    if csrf_token != session.get_csrf_token():
        raise HTTPException(403, "Invalid CSRF token")
    # 执行转账...
`

---

## 第二部分：密码安全

### 2.1 bcrypt

`python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 哈希密码
hashed = pwd_context.hash("my_password")
# ... （每次不同）

# 验证密码
is_valid = pwd_context.verify("my_password", hashed)  # True
is_valid = pwd_context.verify("wrong_password", hashed)  # False
`

### 2.2 argon2（更安全）

`python
# pip install argon2-cffi
from argon2 import PasswordHasher

ph = PasswordHasher()
hashed = ph.hash("my_password")
try:
    ph.verify(hashed, "my_password")
except Exception:
    print("密码错误")
`

### 2.3 密码策略

`python
import re

def validate_password(password: str) -> list[str]:
    errors = []
    if len(password) < 8:
        errors.append("密码至少8个字符")
    if not re.search(r'[A-Z]', password):
        errors.append("需要大写字母")
    if not re.search(r'[a-z]', password):
        errors.append("需要小写字母")
    if not re.search(r'\d', password):
        errors.append("需要数字")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        errors.append("需要特殊字符")
    return errors
`

---

## 第三部分：API 安全

### 3.1 速率限制

`python
from fastapi import Request, HTTPException
import time

request_counts = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    # 清理过期记录
    request_counts[client_ip] = [
        t for t in request_counts.get(client_ip, []) if now - t < 60
    ]
    
    if len(request_counts[client_ip]) >= 100:  # 每分钟 100 次
        raise HTTPException(429, "Too many requests")
    
    request_counts.setdefault(client_ip, []).append(now)
    return await call_next(request)
`

### 3.2 安全响应头

`python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
`

### 3.3 JWT 安全最佳实践

`python
# 1. 密钥足够长且随机
SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # 不要硬编码

# 2. 使用 RS256（非对称）而不是 HS256（对称）在生产环境
from jose import jwt

# HS256（对称）
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# RS256（非对称）
from jose import jwt
private_key = open("private.pem").read()
public_key = open("public.pem").read()
token = jwt.encode(payload, private_key, algorithm="RS256")
payload = jwt.decode(token, public_key, algorithms=["RS256"])

# 3. 设置合理的过期时间
access_token = create_token(data, timedelta(minutes=15))  # 短期
refresh_token = create_token(data, timedelta(days=7))      # 长期

# 4. Token 黑名单（登出）
blacklisted_tokens = set()

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    blacklisted_tokens.add(token)
    return {"message": "Logged out"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(401, "Token revoked")
    # ...
`

---

## 常见错误
1. 密码明文存储 -> 必须哈希
2. SQL 拼接 -> 参数化查询
3. JWT 密钥太短 -> 至少 256 位
4. 没有限流 -> 被 DDoS
5. 没有 HTTPS -> 中间人攻击

## 动手练习
1. 实现 bcrypt 密码哈希
2. 防止 SQL 注入
3. 添加速率限制
4. 实现 JWT 安全策略
