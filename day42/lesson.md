# Day 42 课程：日志 & 监控

## 第一部分：logging 深入

### 1.1 基础配置

`python
import logging

# 基本配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
`

### 1.2 Handler 类型

`python
# 文件 Handler（按大小轮转）
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

file_handler = RotatingFileHandler(
    'app.log', maxBytes=10*1024*1024, backupCount=5  # 10MB, 5个备份
)

# 按时间轮转
time_handler = TimedRotatingFileHandler(
    'app.log', when='midnight', backupCount=30  # 每天，保留30天
)

# Syslog Handler
syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
`

### 1.3 自定义 Formatter

`python
class JSONFormatter(logging.Formatter):
    def format(self, record):
        import json
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)

# 使用
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger('myapp')
logger.addHandler(handler)
`

### 1.4 Filter

`python
class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level
    def filter(self, record):
        return record.levelno == self.level

# 只记录 ERROR
error_handler.addFilter(LevelFilter(logging.ERROR))
`

---

## 第二部分：结构化日志（structlog）

`ash
pip install structlog
`

`python
import structlog

# 配置
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

log = structlog.get_logger()

# 使用
log.info('user_login', user_id=123, ip='192.168.1.1')
log.error('payment_failed', order_id='ORD-001', reason='insufficient_funds')
log.info('api_request', method='GET', path='/users', status=200, duration_ms=42)

# 输出
# {"timestamp": "2024-01-01T00:00:00Z", "event": "user_login", "user_id": 123, "ip": "192.168.1.1"}
`

---

## 第三部分：ELK 基础概念

``
Elasticsearch — 存储和搜索日志
Logstash      — 收集和处理日志
Kibana        — 可视化日志

流程：
应用 -> Filebeat(采集) -> Logstash(处理) -> Elasticsearch(存储) -> Kibana(展示)
``

---

## 第四部分：Prometheus 监控

`python
# pip install prometheus-client

from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# 定义指标
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['path'])
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    ACTIVE_CONNECTIONS.inc()
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    ACTIVE_CONNECTIONS.dec()
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
`

---

## 常见错误
1. 日志没有时间戳 -> 无法定位问题
2. 日志太详细 -> 性能下降
3. 日志没分级 -> 所有信息混在一起
4. 生产环境 print() -> 不可控

## 动手练习
1. 配置 JSON 格式日志
2. 使用 structlog 记录结构化日志
3. 给 FastAPI 添加 Prometheus 中间件
4. 配置日志轮转
