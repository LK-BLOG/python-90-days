# Day 44 安全骨架 - TODO: 实现
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# TODO: 实现密码哈希
def hash_password(password: str) -> str:
    pass

def verify_password(plain: str, hashed: str) -> bool:
    pass

# TODO: 实现速率限制
class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        pass
    
    def is_allowed(self, key: str) -> bool:
        pass

# TODO: 实现输入验证
def sanitize_input(text: str) -> str:
    # 防止 XSS
    pass

# TODO: 实现安全响应头中间件
