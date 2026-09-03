import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Latency')

@app.get('/metrics')
async def metrics():
    return generate_latest()
