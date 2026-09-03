\"\"\"监控配置参考\"\"\"

# Prometheus配置
PROMETHEUS_CONFIG = '''
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: blog-api
    static_configs:
      - targets: ['api:8000']
    metrics_path: /metrics

  - job_name: node-exporter
    static_configs:
      - targets: ['node-exporter:9100']
'''

# 告警规则
ALERT_RULES = '''
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~\"5..\"}[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: \"Error rate > 10%%\"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: \"P95 latency > 1s\"

      - alert: HighMemory
        expr: process_resident_memory_bytes / 1024 / 1024 > 512
        for: 5m
        labels:
          severity: warning
'''

# Grafana Dashboard JSON (简化版)
GRAFANA_DASHBOARD = {
    \"title\": \"Blog API Dashboard\",
    \"panels\": [
        {\"title\": \"Request Rate\", \"type\": \"graph\", \"expr\": \"rate(http_requests_total[5m])\"},
        {\"title\": \"Error Rate\", \"type\": \"graph\", \"expr\": \"rate(http_requests_total{status=~'5..'}[5m])\"},
        {\"title\": \"Latency P95\", \"type\": \"graph\", \"expr\": \"histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))\"},
        {\"title\": \"Active Connections\", \"type\": \"stat\", \"expr\": \"active_connections\"},
    ],
}

print(\"Monitoring config documented\")
