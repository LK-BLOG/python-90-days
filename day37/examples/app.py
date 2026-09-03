# FastAPI 应用 - Docker 化示例
from fastapi import FastAPI

app = FastAPI(title='Docker Demo API')

@app.get('/')
async def root():
    return {'message': 'Hello from Docker!', 'status': 'running'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
