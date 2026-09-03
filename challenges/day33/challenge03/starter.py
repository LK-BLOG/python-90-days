from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
items_db = {}
next_id = 1

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# TODO: 实现 CRUD
# GET /items - 列表
# POST /items - 创建
# GET /items/{id} - 详情
# PUT /items/{id} - 更新
# DELETE /items/{id} - 删除
