# Day 33 课程：FastAPI 基础

## 第一部分：FastAPI 入门

### 1.1 安装和第一个应用

`ash
pip install fastapi uvicorn[standard]
`

`python
# main.py
from fastapi import FastAPI

app = FastAPI(title="My API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
`

`ash
# 启动
uvicorn main:app --reload
# 访问 http://127.0.0.1:8000
# 文档 http://127.0.0.1:8000/docs (Swagger)
# 文档 http://127.0.0.1:8000/redoc (ReDoc)
`

### 1.2 路由系统

`python
from fastapi import FastAPI

app = FastAPI()

# GET - 读取
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# POST - 创建
@app.post("/items/")
async def create_item(name: str, price: float):
    return {"name": name, "price": price, "status": "created"}

# PUT - 更新
@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}

# DELETE - 删除
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"status": "deleted", "item_id": item_id}
`

### 1.3 路径参数 vs 查询参数

`python
@app.get("/users/{user_id}")          # user_id 是路径参数
async def get_user(user_id: int):     # 自动类型转换
    return {"user_id": user_id}

@app.get("/search/")                  # query 是查询参数
async def search(q: str = "", page: int = 1, limit: int = 10):
    return {"q": q, "page": page, "limit": limit}
    # GET /search?q=python&page=2
`

---

## 第二部分：Pydantic 数据验证

### 2.1 请求体模型

`python
from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    email: str = Field(..., description="邮箱")
    age: int = Field(0, ge=0, le=150, description="年龄")
    bio: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    model_config = {"from_attributes": True}  # ORM 模式

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # user 是 UserCreate 实例，已验证
    return {"id": 1, **user.model_dump()}
`

### 2.2 数据验证规则

`python
from pydantic import BaseModel, Field, EmailStr

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)      # 长度限制
    price: float = Field(gt=0)                             # 大于0
    tags: list[str] = Field(default_factory=list)          # 默认空列表
    email: EmailStr                                        # 邮箱格式验证
    quantity: int = Field(ge=0, le=9999)                   # 范围
    description: str = Field(pattern=r"^[a-zA-Z0-9 ]+$")  # 正则
`

### 2.3 查询和路径参数验证

`python
from fastapi import Query, Path

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., ge=1, description="物品ID"),
    q: str = Query(None, max_length=50, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=100, description="每页数量"),
):
    return {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
`

---

## 第三部分：响应模型和状态码

### 3.1 响应模型

`python
from fastapi import HTTPException

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    item = db.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# 多个响应状态码
@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    return db.create(item)
`

### 3.2 常用状态码

`
200 OK            - 成功
201 Created       - 创建成功
204 No Content    - 删除成功（无返回体）
400 Bad Request   - 请求错误
404 Not Found     - 资源不存在
422 Validation Error - 验证错误（FastAPI 自动处理）
500 Server Error  - 服务器错误
`

---

## 第四部分：依赖注入

### 4.1 基础依赖

`python
from fastapi import Depends, Header

async def verify_token(authorization: str = Header()):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)
    return authorization[7:]

@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
    return {"message": "Access granted", "token": token}
`

### 4.2 类依赖

`python
class DatabaseSession:
    def __init__(self):
        self.connection = create_connection()
    
    def query(self, sql):
        return self.connection.execute(sql)
    
    def close(self):
        self.connection.close()

async def get_db():
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def get_users(db: DatabaseSession = Depends(get_db)):
    return db.query("SELECT * FROM users")
`

---

## 第五部分：文件操作

### 5.1 文件上传

`python
from fastapi import UploadFile, File

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type,
    }
`

---

## 常见错误
1. **忘记 await** → async 路由函数中调用同步数据库操作
2. **Pydantic 模型嵌套** → 复杂嵌套结构忘记导入
3. **路径参数类型** → 字符串 "123" 不会自动转 int
4. **响应模型过滤** → 返回了不该暴露的字段

## 动手练习
1. 创建一个 FastAPI 应用，实现 /health 端点
2. 定义 Pydantic 模型，验证用户输入
3. 实现一个完整的 CRUD 端点
4. 添加查询参数验证
5. 用 Depends 实现简单的认证
