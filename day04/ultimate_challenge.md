# Day 4: Boss挑战 — 日志解析器

## 目标
用正则从混合日志中提取结构化数据。

## 功能要求
```python
def parse_log(log_text):
    """解析日志文本，返回结构化数据列表"""
    # 提取：时间戳、日志级别、模块名、消息
```

## 示例
```python
log = """
2024-01-15 10:30:45 [ERROR] database.query: Connection timeout
2024-01-15 10:31:00 [INFO] auth.login: User zhangsan logged in
"""
parse_log(log)
# [{"time": "2024-01-15 10:30:45", "level": "ERROR", "module": "database.query", "msg": "Connection timeout"}, ...]
```
