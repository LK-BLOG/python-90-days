# 示例：JSON基础操作
import json
from datetime import datetime

# 1. 基础JSON操作
print("=== 基础JSON操作 ===")
data = {
    "name": "张三",
    "age": 25,
    "scores": [90, 85, 92],
    "address": {
        "city": "北京",
        "street": "中关村大街"
    }
}

# 序列化
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("序列化:")
print(json_str)

# 反序列化
parsed = json.loads(json_str)
print("\n反序列化:")
print(parsed)

# 2. 文件操作
print("\n=== 文件操作 ===")
filename = "test_data.json"

# 写入文件
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"数据已写入 {filename}")

# 读取文件
with open(filename, 'r', encoding='utf-8') as f:
    loaded = json.load(f)
print(f"从文件读取: {loaded}")

# 3. 自定义编码器
print("\n=== 自定义编码器 ===")
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data_with_datetime = {
    "event": "会议",
    "time": datetime.now(),
    "tags": {"重要", "紧急"}
}

# 注意：集合不能直接JSON序列化
try:
    json.dumps(data_with_datetime)
except TypeError as e:
    print(f"序列化失败: {e}")

# 使用自定义编码器
json_str = json.dumps(data_with_datetime, cls=DateTimeEncoder, ensure_ascii=False)
print(f"使用自定义编码器: {json_str}")

# 清理
import os
if os.path.exists(filename):
    os.unlink(filename)

print("\n演示完成")
