# -*- coding: utf-8 -*-
# Day 1 示例3: *args 和 **kwargs

def debug_info(*args, **kwargs):
    """打印所有传入的参数"""
    print(f"位置参数 (tuple): {args}")
    print(f"关键字参数 (dict): {kwargs}")

debug_info(1, 2, 3, name="张三", age=25)
print()

# 综合示例：灵活的日志函数
def log(level, *messages, **extra):
    msg_text = " | ".join(str(m) for m in messages)
    extra_text = " ".join(f"{k}={v}" for k, v in extra.items())
    print(f"[{level}] {msg_text} {extra_text}")

log("INFO", "用户登录", "IP:192.168.1.1")
log("ERROR", "数据库连接失败", "重试中", retries=3, timeout=30)
