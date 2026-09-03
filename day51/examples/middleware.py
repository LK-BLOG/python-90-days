\"\"\"自定义中间件集合\"\"\"

import time
import uuid
import logging
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class RequestLogger:
    \"\"\"请求日志中间件\"\"\"

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope[\"type\"] != \"http\":
            return await self.app(scope, receive, send)

        start = time.time()
        request = Request(scope, receive)
        method = request.method
        path = request.url.path

        response = await self.app(scope, receive, send)
        duration = time.time() - start

        logger.info(f\"{method} {path} {duration:.3f}s\")
        return response


class RequestIDMiddleware:
    \"\"\"请求ID中间件\"\"\"

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope[\"type\"] != \"http\":
            return await self.app(scope, receive, send)

        request = Request(scope, receive)
        rid = request.headers.get(\"X-Request-ID\", str(uuid.uuid4()))

        async def send_wrapper(message):
            if message[\"type\"] == \"http.response.start\":
                headers = dict(message.get(\"headers\", []))
                headers[b\"x-request-id\"] = rid.encode()
                message[\"headers\"] = list(headers.items())
            await send(message)

        scope[\"request_id\"] = rid
        return await self.app(scope, receive, send_wrapper)


class RateLimitMiddleware:
    \"\"\"速率限制中间件\"\"\"

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        self.app = app
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    async def __call__(self, scope, receive, send):
        if scope[\"type\"] != \"http\":
            return await self.app(scope, receive, send)

        request = Request(scope, receive)
        client_ip = request.client.host if request.client else \"unknown\"
        now = time.time()

        # 清理过期记录
        self._requests[client_ip] = [
            t for t in self._requests[client_ip] if now - t < self.window
        ]

        if len(self._requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={\"detail\": \"Too many requests\"}
            )

        self._requests[client_ip].append(now)
        return await self.app(scope, receive, send)


class ErrorHandlerMiddleware:
    \"\"\"错误处理中间件\"\"\"

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            return await self.app(scope, receive, send)
        except Exception as e:
            logger.exception(f\"Unhandled error: {e}\")
            return JSONResponse(
                status_code=500,
                content={\"detail\": \"Internal server error\", \"type\": type(e).__name__}
            )


# 注册中间件
def register_middleware(app):
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RequestLogger)
