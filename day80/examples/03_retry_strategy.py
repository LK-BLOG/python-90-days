# Day 80 示例 3: 重试策略
import time, random
from functools import wraps

def retry(max_retries=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'  ⚠️ 尝试{attempt+1}失败: {e}')
                    if attempt < max_retries - 1:
                        print(f'  ⏳ 等待{current_delay:.1f}s...')
                        time.sleep(current_delay)
                        current_delay *= backoff
            raise Exception('所有重试都失败')
        return wrapper
    return decorator

@retry(max_retries=3, delay=0.1)
def unreliable_api():
    if random.random() < 0.7:
        raise ConnectionError('网络错误')
    return '成功!'

if __name__ == '__main__':
    try:
        print(unreliable_api())
    except Exception as e:
        print(f'最终失败: {e}')
