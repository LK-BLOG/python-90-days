# Day 44 安全示例
from passlib.context import CryptContext
import re
import time

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# 密码哈希
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 密码策略
def validate_password(password: str) -> list:
    errors = []
    if len(password) < 8: errors.append('至少8个字符')
    if not re.search(r'[A-Z]', password): errors.append('需要大写字母')
    if not re.search(r'[a-z]', password): errors.append('需要小写字母')
    if not re.search(r'\d', password): errors.append('需要数字')
    return errors

# 速率限制
class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        self.requests[key] = [t for t in self.requests.get(key, []) if now - t < self.window]
        if len(self.requests[key]) >= self.max_requests:
            return False
        self.requests[key].append(now)
        return True

if __name__ == '__main__':
    h = hash_password('MyPass123!')
    print(f'Hash: {h[:20]}...')
    print(f'Verify correct: {verify_password(\"MyPass123!\", h)}')
    print(f'Verify wrong: {verify_password(\"wrong\", h)}')
    print(f'Policy: {validate_password(\"abc\")}')
