# Day 39 REST API 设计示例 - 博客系统
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title='Blog API', version='1.0.0', description='RESTful 博客 API')

# 模型
class PostCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    tags: list[str]
    created_at: str

# 模拟数据
posts_db = []
next_id = 1

# 资源路由：RESTful 风格
@app.get('/posts', response_model=dict, summary='获取文章列表')
async def list_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    tag: Optional[str] = Query(None, description='按标签过滤'),
    sort_by: str = Query('created_at', description='排序字段'),
    order: str = Query('desc', regex='^(asc|desc)$'),
):
    global posts_db
    filtered = posts_db
    if tag:
        filtered = [p for p in filtered if tag in p.get('tags', [])]
    total = len(filtered)
    start = (page - 1) * per_page
    items = filtered[start:start + per_page]
    return {
        'data': items,
        'pagination': {'total': total, 'page': page, 'per_page': per_page, 'total_pages': -(-total // per_page)}
    }

@app.post('/posts', status_code=201, response_model=PostResponse, summary='创建文章')
async def create_post(post: PostCreate):
    global next_id
    new_post = {'id': next_id, 'author_id': 1, 'created_at': datetime.now().isoformat(), **post.model_dump()}
    posts_db.append(new_post)
    next_id += 1
    return new_post

@app.get('/posts/{post_id}', response_model=PostResponse, summary='获取文章详情')
async def get_post(post_id: int):
    for p in posts_db:
        if p['id'] == post_id:
            return p
    raise HTTPException(404, 'Post not found')

@app.put('/posts/{post_id}', response_model=PostResponse, summary='更新文章')
async def update_post(post_id: int, post: PostCreate):
    for p in posts_db:
        if p['id'] == post_id:
            p.update(post.model_dump())
            return p
    raise HTTPException(404, 'Post not found')

@app.delete('/posts/{post_id}', status_code=204, summary='删除文章')
async def delete_post(post_id: int):
    global posts_db
    posts_db = [p for p in posts_db if p['id'] != post_id]

# 子资源路由
@app.get('/posts/{post_id}/comments', summary='获取文章评论')
async def get_comments(post_id: int):
    return {'data': [], 'post_id': post_id}

@app.post('/posts/{post_id}/comments', status_code=201, summary='添加评论')
async def add_comment(post_id: int, content: str):
    return {'id': 1, 'post_id': post_id, 'content': content}
