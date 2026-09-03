# Day 37 Docker 骨架
# TODO: 为以下应用创建 Dockerfile 和 docker-compose.yml
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello'}

@app.get('/health')
async def health():
    return {'status': 'ok'}
