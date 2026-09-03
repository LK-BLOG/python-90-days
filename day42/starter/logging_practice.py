# Day 42 日志监控骨架
import logging
import json

# TODO: 实现 JSON Formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        # TODO: 返回 JSON 格式日志
        pass

# TODO: 配置日志系统
def setup_logging():
    # TODO: 创建 logger
    # TODO: 添加 Handler（文件 + 控制台）
    # TODO: 设置 Formatter
    # TODO: 配置日志轮转
    pass

# TODO: 实现 Prometheus 指标
# TODO: 实现 /metrics 端点
# TODO: 实现 /health 端点
