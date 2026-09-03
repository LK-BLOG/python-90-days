\"\"\"Day 51 Starter: 中间件和测试练习\"\"\"

# TODO: 实现以下中间件

# 1. 请求日志中间件
class RequestLogger:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        pass  # 实现: 记录method/path/status/duration

# 2. 请求ID中间件
class RequestIDMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        pass  # 实现: 生成/传递X-Request-ID

# 3. 速率限制中间件
class RateLimitMiddleware:
    def __init__(self, app, max_requests=100, window_seconds=60):
        self.app = app
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests = {}

    async def __call__(self, scope, receive, send):
        pass  # 实现: 限制每IP每分钟请求数
