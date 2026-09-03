# Day 36 Redis 缓存示例
import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 模拟数据库
db_users = {1: {'id': 1, 'name': 'Alice', 'age': 30}, 2: {'id': 2, 'name': 'Bob', 'age': 25}}

def get_user_cached(user_id):
    cache_key = f'user:{user_id}'
    # 尝试缓存
    cached = r.get(cache_key)
    if cached:
        print(f'  [CACHE HIT] user:{user_id}')
        return json.loads(cached)
    # 缓存未命中，查 DB
    print(f'  [CACHE MISS] user:{user_id}')
    user = db_users.get(user_id)
    if user:
        r.setex(cache_key, 300, json.dumps(user))  # 5 分钟过期
    return user

# 演示
print('第一次读取（缓存未命中）:')
print(get_user_cached(1))
print('第二次读取（缓存命中）:')
print(get_user_cached(1))
