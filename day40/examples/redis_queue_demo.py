# Day 40 Redis 消息队列示例
import redis
import json

r = redis.Redis(decode_responses=True)

def produce(queue, task):
    r.lpush(queue, json.dumps(task))
    print(f'Produced: {task}')

def consume(queue):
    while True:
        _, data = r.brpop(queue, timeout=5)
        if data:
            task = json.loads(data)
            print(f'Consumed: {task}')
            return task

if __name__ == '__main__':
    produce('tasks', {'action': 'send_email', 'to': 'test@test.com'})
    produce('tasks', {'action': 'process', 'data': [1,2,3]})
    consume('tasks')
