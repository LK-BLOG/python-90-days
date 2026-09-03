\"\"\"安全中间件\"\"\"

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address


def setup_security(app):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[\"https://myapp.com\", \"http://localhost:3000\"],
        allow_methods=[\"GET\", \"POST\", \"PUT\", \"DELETE\"],
        allow_headers=[\"Authorization\", \"Content-Type\"],
        allow_credentials=True,
        max_age=600,
    )

    # 速率限制
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter

    return app


@app.middleware(\"http\")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers[\"X-Content-Type-Options\"] = \"nosniff\"
    response.headers[\"X-Frame-Options\"] = \"DENY\"
    response.headers[\"X-XSS-Protection\"] = \"1; mode=block\"
    response.headers[\"Strict-Transport-Security\"] = \"max-age=31536000\"
    response.headers[\"Content-Security-Policy\"] = \"default-src 'self'\"
    response.headers[\"Referrer-Policy\"] = \"strict-origin-when-cross-origin\"
    return response
