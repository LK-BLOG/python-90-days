# Day 39 REST API 设计骨架 - TODO: 实现
from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title='Blog API')

class PostCreate(BaseModel):
    title: str
    content: str

# TODO: 实现以下端点
# GET    /posts          - 文章列表（分页+过滤+排序）
# POST   /posts          - 创建文章
# GET    /posts/{id}     - 文章详情
# PUT    /posts/{id}     - 更新文章
# DELETE /posts/{id}     - 删除文章
# GET    /posts/{id}/comments - 文章评论
# POST   /posts/{id}/comments - 添加评论

@app.get('/posts')
async def list_posts(page: int = 1, per_page: int = 10):
    # TODO: 实现分页
    pass

@app.post('/posts', status_code=201)
async def create_post(post: PostCreate):
    # TODO: 实现
    pass
