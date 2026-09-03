\"\"\"JWT认证模块\"\"\"

import jwt
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = \"your-secret-key-change-in-production\"
ALGORITHM = \"HS256\"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({\"exp\": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# 密码哈希（用bcrypt）
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=[\"bcrypt\"], deprecated=\"auto\")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


if __name__ == \"__main__\":
    # 测试token
    token = create_access_token({\"sub\": \"1\", \"username\": \"alice\"})
    print(f\"Token: {token[:50]}...\")

    payload = decode_token(token)
    print(f\"Payload: {payload}\")

    # 测试密码
    hashed = hash_password(\"mypassword\")
    print(f\"Hashed: {hashed}\")
    print(f\"Verify: {verify_password('mypassword', hashed)}\")
