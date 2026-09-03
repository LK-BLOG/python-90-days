# Day 9 完整教学：JSON数据处理

## 1. JSON基础
### 1.1 JSON与Python数据类型对应
**对应关系**：
- JSON对象 → Python字典
- JSON数组 → Python列表
- JSON字符串 → Python字符串
- JSON数字 → Python整数/浮点数
- JSON布尔值 → Python布尔值
- JSON null → Python None

**示例**：
```python
import json

# Python字典转JSON
python_dict = {
    "name": "张三",
    "age": 25,
    "is_student": False,
    "scores": [90, 85, 92],
    "address": {
        "city": "北京",
        "street": "中关村大街"
    }
}

json_str = json.dumps(python_dict, ensure_ascii=False, indent=2)
print(json_str)

# JSON转Python字典
python_obj = json.loads(json_str)
print(python_obj["name"])  # 张三
```

### 1.2 json.dumps()和json.loads()
**说明**：字符串形式的JSON转换。

**语法**：
```python
# 转换为JSON字符串
json_str = json.dumps(obj, ensure_ascii=False, indent=2)

# 从JSON字符串转换
obj = json.loads(json_str)
```

**常用参数**：
- `ensure_ascii=False`：支持中文
- `indent=2`：格式化输出
- `sort_keys=True`：按键排序

**示例**：
```python
import json

data = {"name": "李四", "scores": [95, 88, 92]}

# 转换为JSON字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# 从JSON字符串转换
parsed = json.loads(json_str)
print(parsed)
```

### 1.3 json.dump()和json.load()
**说明**：文件形式的JSON转换。

**语法**：
```python
# 写入JSON文件
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

# 从JSON文件读取
with open('data.json', 'r', encoding='utf-8') as f:
    obj = json.load(f)
```

**示例**：
```python
import json

# 准备数据
data = {
    "users": [
        {"name": "王五", "age": 30},
        {"name": "赵六", "age": 28}
    ]
}

# 写入文件
with open('users.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取文件
with open('users.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)
    print(loaded_data)
```

## 2. 自定义JSONEncoder
### 2.1 基础自定义编码器
**说明**：处理Python特有类型（如日期、集合等）。

**语法**：
```python
import json
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)
```

**示例**：
```python
import json
from datetime import datetime
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # 处理日期时间
        if isinstance(obj, datetime):
            return {
                "__type__": "datetime",
                "value": obj.isoformat()
            }
        # 处理Decimal
        if isinstance(obj, Decimal):
            return float(obj)
        # 处理集合
        if isinstance(obj, set):
            return {
                "__type__": "set",
                "value": list(obj)
            }
        return super().default(obj)

# 使用自定义编码器
data = {
    "name": "测试",
    "created_at": datetime.now(),
    "tags": {"python", "json", "编码"},
    "price": Decimal("99.99")
}

json_str = json.dumps(data, cls=CustomEncoder, ensure_ascii=False, indent=2)
print(json_str)
```

### 2.2 自定义解码器
**说明**：还原Python特有类型。

**语法**：
```python
def custom_decoder(dct):
    if "__type__" in dct:
        if dct["__type__"] == "datetime":
            return datetime.fromisoformat(dct["value"])
        if dct["__type__"] == "set":
            return set(dct["value"])
    return dct
```

**示例**：
```python
import json
from datetime import datetime

def custom_decoder(dct):
    """自定义解码器"""
    if "__type__" in dct:
        type_name = dct["__type__"]
        if type_name == "datetime":
            return datetime.fromisoformat(dct["value"])
        if type_name == "set":
            return set(dct["value"])
        if type_name == "bytes":
            return bytes(dct["value"])
    return dct

# 解码JSON
json_str = '''
{
    "name": "测试",
    "created_at": {"__type__": "datetime", "value": "2024-01-15T10:30:00"},
    "tags": {"__type__": "set", "value": ["python", "json"]}
}
'''

data = json.loads(json_str, object_hook=custom_decoder)
print(type(data["created_at"]))  # <class 'datetime.datetime'>
print(type(data["tags"]))  # <class 'set'>
```

## 3. 数据验证
### 3.1 简单验证
**示例**：
```python
def validate_user_data(data):
    """验证用户数据"""
    errors = []
    
    # 检查必填字段
    required_fields = ["name", "age", "email"]
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必填字段: {field}")
    
    # 验证类型
    if "age" in data and not isinstance(data["age"], int):
        errors.append("年龄必须是整数")
    
    if "email" in data and not isinstance(data["email"], str):
        errors.append("邮箱必须是字符串")
    
    # 验证范围
    if "age" in data and (data["age"] < 0 or data["age"] > 150):
        errors.append("年龄必须在0-150之间")
    
    return errors

# 使用示例
user_data = {"name": "张三", "age": "25", "email": "test@example.com"}
errors = validate_user_data(user_data)
if errors:
    print("验证错误:", errors)
else:
    print("验证通过")
```

### 3.2 JSON Schema验证
**说明**：使用JSON Schema进行数据验证。

**示例**：
```python
import json

# 定义Schema
user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "age": {"type": "integer", "minimum": 0, "maximum": 150},
        "email": {"type": "string", "format": "email"},
        "tags": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["name", "age", "email"]
}

def validate_with_schema(data, schema):
    """使用Schema验证数据"""
    # 简单验证实现
    errors = []
    
    # 验证类型
    if schema.get("type") == "object":
        if not isinstance(data, dict):
            errors.append("数据必须是对象")
            return errors
        
        # 验证必填字段
        for field in schema.get("required", []):
            if field not in data:
                errors.append(f"缺少必填字段: {field}")
        
        # 验证属性
        for field, field_schema in schema.get("properties", {}).items():
            if field in data:
                field_errors = validate_field(data[field], field_schema, field)
                errors.extend(field_errors)
    
    return errors

def validate_field(value, schema, field_name):
    """验证单个字段"""
    errors = []
    
    # 验证类型
    expected_type = schema.get("type")
    if expected_type == "string" and not isinstance(value, str):
        errors.append(f"{field_name}必须是字符串")
    elif expected_type == "integer" and not isinstance(value, int):
        errors.append(f"{field_name}必须是整数")
    elif expected_type == "array" and not isinstance(value, list):
        errors.append(f"{field_name}必须是数组")
    
    # 验证范围
    if "minimum" in schema and value < schema["minimum"]:
        errors.append(f"{field_name}不能小于{schema['minimum']}")
    if "maximum" in schema and value > schema["maximum"]:
        errors.append(f"{field_name}不能大于{schema['maximum']}")
    
    return errors

# 使用示例
user_data = {
    "name": "张三",
    "age": 25,
    "email": "zhangsan@example.com",
    "tags": ["python", "json"]
}

errors = validate_with_schema(user_data, user_schema)
print("验证结果:", "通过" if not errors else errors)
```

## 4. 处理循环引用
### 4.1 检测循环引用
**示例**：
```python
import json

def detect_circular_reference(obj, seen=None):
    """检测循环引用"""
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return True
    
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        for value in obj.values():
            if detect_circular_reference(value, seen.copy()):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if detect_circular_reference(item, seen.copy()):
                return True
    
    return False

# 创建循环引用
a = {"name": "a"}
b = {"name": "b", "ref": a}
a["ref"] = b  # 循环引用

print("存在循环引用:", detect_circular_reference(a))
```

### 4.2 处理循环引用
**示例**：
```python
import json

class CircularEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = set()
    
    def default(self, obj):
        obj_id = id(obj)
        if obj_id in self.seen:
            return {"__circular__": True}
        self.seen.add(obj_id)
        return super().default(obj)

# 使用示例
a = {"name": "a"}
b = {"name": "b", "ref": a}
a["ref"] = b

try:
    json_str = json.dumps(a, cls=CircularEncoder, indent=2)
    print("序列化成功")
except TypeError as e:
    print(f"序列化失败: {e}")
```

## 5. 日期时间序列化
### 5.1 基础日期序列化
**示例**：
```python
import json
from datetime import datetime, date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# 使用示例
data = {
    "name": "会议",
    "start_time": datetime(2024, 1, 15, 10, 30, 0),
    "end_time": datetime(2024, 1, 15, 12, 0, 0),
    "date": date(2024, 1, 15)
}

json_str = json.dumps(data, cls=DateEncoder, ensure_ascii=False, indent=2)
print(json_str)

# 解析
parsed = json.loads(json_str)
print(parsed)
```

### 5.2 高级日期处理
**示例**：
```python
import json
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

class AdvancedDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                "__type__": "datetime",
                "iso": obj.isoformat(),
                "timestamp": obj.timestamp()
            }
        if isinstance(obj, timedelta):
            return {
                "__type__": "timedelta",
                "total_seconds": obj.total_seconds()
            }
        return super().default(obj)

def date_hook(dct):
    """日期解析钩子"""
    if "__type__" in dct:
        if dct["__type__"] == "datetime":
            return datetime.fromisoformat(dct["iso"])
        if dct["__type__"] == "timedelta":
            return timedelta(seconds=dct["total_seconds"])
    return dct

# 使用示例
data = {
    "event": "项目截止",
    "deadline": datetime(2024, 2, 1, 18, 0, 0),
    "duration": timedelta(days=30, hours=12)
}

json_str = json.dumps(data, cls=AdvancedDateEncoder, indent=2)
parsed = json.loads(json_str, object_hook=date_hook)

print("原始数据:", data)
print("解析后:", parsed)
```

## 6. 实际应用：Todo系统JSON持久化
```python
import json
from datetime import datetime
from pathlib import Path

class TodoJSONStorage:
    """Todo JSON存储"""
    
    def __init__(self, filename="todos.json"):
        self.filename = Path(filename)
        self.todos = []
        self.load()
    
    def load(self):
        """从JSON文件加载"""
        try:
            if self.filename.exists():
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 转换日期字符串为datetime对象
                    for todo in data:
                        if "created_at" in todo and todo["created_at"]:
                            todo["created_at"] = datetime.fromisoformat(todo["created_at"])
                        if "completed_at" in todo and todo["completed_at"]:
                            todo["completed_at"] = datetime.fromisoformat(todo["completed_at"])
                    self.todos = data
        except Exception as e:
            print(f"加载失败: {e}")
            self.todos = []
    
    def save(self):
        """保存到JSON文件"""
        try:
            # 转换datetime对象为字符串
            data_to_save = []
            for todo in self.todos:
                todo_copy = todo.copy()
                if "created_at" in todo_copy and isinstance(todo_copy["created_at"], datetime):
                    todo_copy["created_at"] = todo_copy["created_at"].isoformat()
                if "completed_at" in todo_copy and isinstance(todo_copy["completed_at"], datetime):
                    todo_copy["completed_at"] = todo_copy["completed_at"].isoformat()
                data_to_save.append(todo_copy)
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def add_todo(self, title, priority="中"):
        """添加Todo"""
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now(),
            "completed_at": None
        }
        self.todos.append(todo)
        self.save()
        return todo

# 使用示例
if __name__ == "__main__":
    storage = TodoJSONStorage("demo_todos.json")
    
    # 添加Todo
    todo1 = storage.add_todo("学习JSON", "高")
    todo2 = storage.add_todo("完成练习", "中")
    
    print("添加成功:")
    for todo in storage.todos:
        print(f"  {todo['id']}. {todo['title']} ({todo['priority']})")
    
    # 重新加载验证
    storage2 = TodoJSONStorage("demo_todos.json")
    print(f"\n重新加载后: {len(storage2.todos)} 个Todo")
    
    # 清理
    import os
    os.unlink("demo_todos.json")
```

## 7. 常见错误与调试
1. **编码问题**：始终使用`ensure_ascii=False`
2. **类型不支持**：自定义Encoder处理特殊类型
3. **循环引用**：检测并处理循环引用
4. **日期格式**：统一使用ISO格式
5. **文件权限**：确保文件可读写

## 8. 动手练习
1. 实现自定义JSON编解码器
2. 创建JSON数据验证器
3. 实现配置文件的JSON存储
4. 处理复杂的嵌套数据结构
5. 实现增量JSON更新

---
**提示**：JSON是数据交换的基础，掌握它能让你的程序更强大！
