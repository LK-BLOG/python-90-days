import logging
import json
from datetime import datetime

# JSON Formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
        }
        return json.dumps(log_data, ensure_ascii=False)

# 配置
def setup_logging(level=logging.INFO):
    logger = logging.getLogger('myapp')
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    log = setup_logging()
    log.info('Application started')
    log.warning('Low disk space')
    log.error('Database connection failed')
