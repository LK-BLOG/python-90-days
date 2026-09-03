\"\"\"FastAPI 依赖注入示例\"\"\"

from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Optional

app = FastAPI()

# 模拟数据库
fake_db = {
    1: {\"id\": 1, \"name\": \"Alice\", \"role\": \"admin\"},
    2: {\"id\": 2, \"name\": \"Bob\", \"role\": \"user\"},
}

# 依赖：获取当前用户
async def get_current_user(authorization: str = None):
    if not authorization:
        raise HTTPException(status_code=401, detail=\"未认证\")
    # 简化：用 authorization 作为 user_id
    user_id = int(authorization)
    if user_id not in fake_db:
        raise HTTPException(status_code=401, detail=\"用户不存在\")
    return fake_db[user_id]

# 依赖：检查管理员权限
async def require_admin(user: dict = Depends(get_current_user)):
    if user[\"role\"] != \"admin\":
        raise HTTPException(status_code=403, detail=\"需要管理员权限\")
    return user

# 依赖：分页参数
def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    return {\"skip\": skip, \"limit\": limit}

@app.get(\"/users/\")
async def list_users(pagination: dict = Depends(pagination)):
    users = list(fake_db.values())
    return users[pagination[\"skip\"]:pagination[\"skip\"]+pagination[\"limit\"]]

@app.get(\"/admin/stats\")
async def admin_stats(admin: dict = Depends(require_admin)):
    return {\"total_users\": len(fake_db), \"admin\": admin[\"name\"]}
