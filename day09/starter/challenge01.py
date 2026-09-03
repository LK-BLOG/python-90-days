# Day 9 挑战一：自定义 JSON 编解码器 (★★★☆☆)
# 要求: 支持 datetime/set/Decimal 等特殊类型的 JSON 序列化。


import json
from datetime import datetime, date
from decimal import Decimal


class CustomEncoder(json.JSONEncoder):
    """自定义 JSON 编码器 —— 支持特殊类型。"""
    
    def default(self, obj):
        """处理 json 默认无法序列化的类型。
        
        支持:
            - datetime/date -> ISO 格式字符串
            - set/frozenset -> 列表
            - Decimal -> 字符串
            - bytes -> Base64 或 hex
            - 自定义对象 -> 调用 to_dict()
        """
        # TODO: 用 isinstance 逐类型处理
        pass


def custom_dumps(obj, **kwargs):
    """使用自定义编码器的 dumps 包装。"""
    return json.dumps(obj, cls=CustomEncoder, ensure_ascii=False, **kwargs)


def custom_loads(s, object_hook=None):
    """带 object_hook 的 loads 包装。
    
    object_hook 应该处理:
        - ISO 日期字符串 -> datetime
        - _type 标记 -> 对应类型还原
    """
    # TODO: 实现 object_hook 处理特殊类型还原
    pass


class JSONFile:
    """支持特殊类型的 JSON 文件读写工具。"""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def save(self, data, indent=2):
        """保存数据到 JSON 文件。"""
        # TODO: 使用 custom_dumps 写入
        pass
    
    def load(self):
        """从 JSON 文件加载数据。"""
        # TODO: 使用 custom_loads 读取
        pass
    
    def update(self, key, value):
        """读取 -> 更新某个键 -> 保存。"""
        pass


# ===== 测试 =====
if __name__ == "__main__":
    data = {
        "name": "测试",
        "date": datetime(2024, 1, 15, 10, 30),
        "tags": {"python", "json", "test"},
        "price": Decimal("99.99"),
        "items": [{"created": date(2024, 6, 1)}, {"created": date(2024, 12, 25)}]
    }
    
    json_str = custom_dumps(data)
    print("序列化:")
    print(json_str)
    
    restored = custom_loads(json_str)
    print(f"\n还原 date 类型: {type(restored['date'])}")
    print(f"还原 tags 类型: {type(restored['tags'])}")
