# 多阶段构建Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# 运行阶段
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

# 非root用户
RUN useradd -m appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s CMD python -c \"import httpx; httpx.get('http://localhost:8000/health')\"

CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\", \"--workers\", \"4\"]
