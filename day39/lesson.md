# Day 39 课程：REST API 设计

## 第一部分：REST 设计原则

### 1.1 资源命名

# 好的命名：
GET    /users           # 用户列表
GET    /users/123       # 单个用户
POST   /users           # 创建用户
PUT    /users/123       # 更新用户
DELETE /users/123       # 删除用户

GET    /users/123/orders         # 用户的订单
POST   /users/123/orders         # 为用户创建订单
GET    /users/123/orders/456     # 用户的某个订单

# 不好的命名：
GET /getUser            # 不用动词
POST /deleteUser/123    # 不用动词
GET /user_list          # 用复数名词

### 1.2 HTTP 方法和状态码

| 方法 | 用途 | 成功状态码 |
|------|------|-----------|
| GET | 读取 | 200 OK |
| POST | 创建 | 201 Created |
| PUT | 全量更新 | 200 OK |
| PATCH | 部分更新 | 200 OK |
| DELETE | 删除 | 204 No Content |

错误状态码：
- 400 Bad Request — 客户端错误
- 401 Unauthorized — 未认证
- 403 Forbidden — 无权限
- 404 Not Found — 资源不存在
- 409 Conflict — 冲突（如重复创建）
- 422 Unprocessable Entity — 验证失败
- 429 Too Many Requests — 限流
- 500 Internal Server Error — 服务器错误

### 1.3 响应格式

`json
{
    "data": { "id": 1, "name": "Alice" },
    "meta": { "request_id": "abc-123" }
}

// 列表
{
    "data": [...],
    "pagination": {
        "total": 100,
        "page": 1,
        "per_page": 10,
        "total_pages": 10
    }
}

// 错误
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": [
            {"field": "email", "message": "Invalid email format"}
        ]
    }
}
`

---

## 第二部分：分页、过滤、排序

### 2.1 分页

`python
from fastapi import Query

@app.get("/users/")
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(20, ge=1, le=100, description="每页数量"),
):
    offset = (page - 1) * per_page
    users = db.query(User).offset(offset).limit(per_page).all()
    total = db.query(User).count()
    return {
        "data": users,
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
        }
    }
`

### 2.2 过滤和排序

`python
@app.get("/users/")
async def list_users(
    status: str = Query(None, description="状态过滤"),
    min_age: int = Query(None, description="最小年龄"),
    sort_by: str = Query("id", description="排序字段"),
    order: str = Query("asc", regex="^(asc|desc)$"),
):
    query = db.query(User)
    if status:
        query = query.filter(User.status == status)
    if min_age:
        query = query.filter(User.age >= min_age)
    
    # 排序
    sort_column = getattr(User, sort_by, User.id)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    return query.all()
`

---

## 第三部分：版本控制

### 3.1 URL 版本

`python
# /api/v1/users
# /api/v2/users
app_v1 = FastAPI()
app_v2 = FastAPI()

@app_v1.get("/users/")
async def list_users_v1():
    return {"users": [...]}  # v1 格式

@app_v2.get("/users/")
async def list_users_v2():
    return {"data": [...], "pagination": {...}}  # v2 格式
`

### 3.2 Header 版本

`python
from fastapi import Header

@app.get("/users/")
async def list_users(accept_version: str = Header("1.0")):
    if accept_version.startswith("2"):
        return {"data": [...]}
    return {"users": [...]}
`

---

## 第四部分：OpenAPI 文档

`python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="My API",
    description="一个用户管理 API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 自定义 OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # 添加自定义扩展
    schema["info"]["x-logo"] = {"url": "https://example.com/logo.png"}
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
`

---

## 常见错误
1. 用动词命名资源 -> GET /getUser -> GET /users/{id}
2. 状态码乱用 -> 创建返回 200 -> 应该 201
3. 没有分页 -> 大量数据拖垮性能
4. 没有版本控制 -> 破坏性变更影响现有用户

## 动手练习
1. 设计一个博客系统的 REST API
2. 实现分页和过滤
3. 添加版本控制
4. 自定义 OpenAPI 文档
