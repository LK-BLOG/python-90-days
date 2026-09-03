\"\"\"结构化日志示例\"\"\"

import logging
import json
import time
import uuid
from datetime import datetime


class JSONFormatter(logging.Formatter):
    \"\"\"JSON格式日志\"\"\"

    def format(self, record):
        log_data = {
            \"timestamp\": datetime.utcnow().isoformat(),
            \"level\": record.levelname,
            \"logger\": record.name,
            \"message\": record.getMessage(),
            \"module\": record.module,
            \"function\": record.funcName,
            \"line\": record.lineno,
        }

        # 添加额外字段
        if hasattr(record, \"request_id\"):
            log_data[\"request_id\"] = record.request_id
        if hasattr(record, \"method\"):
            log_data[\"method\"] = record.method
        if hasattr(record, \"path\"):
            log_data[\"path\"] = record.path
        if hasattr(record, \"status_code\"):
            log_data[\"status_code\"] = record.status_code
        if hasattr(record, \"duration\"):
            log_data[\"duration\"] = record.duration

        if record.exc_info:
            log_data[\"exception\"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(level: str = \"INFO\") -> logging.Logger:
    logger = logging.getLogger(\"app\")
    logger.setLevel(getattr(logging, level.upper()))

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    return logger


# 请求日志中间件
class RequestLogger:
    def __init__(self, app, logger=None):
        self.app = app
        self.logger = logger or setup_logging()

    async def __call__(self, scope, receive, send):
        if scope[\"type\"] != \"http\":
            return await self.app(scope, receive, send)

        request_id = str(uuid.uuid4())[:8]
        start = time.time()

        async def send_wrapper(message):
            if message[\"type\"] == \"http.response.start\":
                duration = round(time.time() - start, 3)
                self.logger.info(
                    f\"Request completed\",
                    extra={
                        \"request_id\": request_id,
                        \"method\": scope[\"method\"],
                        \"path\": scope[\"path\"],
                        \"status_code\": message[\"status\"],
                        \"duration\": duration,
                    },
                )
            await send(message)

        return await self.app(scope, receive, send_wrapper)


if __name__ == \"__main__\":
    logger = setup_logging()
    logger.info(\"Application started\")
    logger.info(\"User login\", extra={\"user_id\": 42, \"ip\": \"192.168.1.1\"})
    logger.warning(\"Slow query\", extra={\"query\": \"SELECT ...\", \"duration\": 2.5})
    logger.error(\"Connection failed\", extra={\"host\": \"db.example.com\", \"port\": 5432})
