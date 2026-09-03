"""示例2：pdb 调试"""
import pdb

def buggy_function(data):
    """一个有 Bug 的函数"""
    result = []
    
    for i, item in enumerate(data):
        # 假设这里有个 Bug
        processed = item / 2  # 如果 item 是字符串就会出错
        result.append(processed)
    
    return result

def debug_example():
    """调试示例"""
    data = [1, 2, 3, 4, 5]
    
    # 方法1：设置断点
    # pdb.set_trace()  # 取消注释来调试
    
    # 方法2：条件断点
    for i, item in enumerate(data):
        if i == 3:  # 在第4个元素时中断
            # pdb.set_trace()  # 取消注释
            pass
    
    result = buggy_function(data)
    return result

# 使用 icecream 调试（更好的 print 调试）
try:
    from icecream import ic
except ImportError:
    # 如果没安装 icecream，定义一个简单的替代
    def ic(*args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                print(f"ic| {k}: {v}")
        elif len(args) == 1:
            print(f"ic| {args[0]}")
        else:
            print(f"ic| {args}")

def better_debug_example():
    """更好的调试方式"""
    data = [1, 2, 3, 4, 5]
    
    ic(data)
    
    result = []
    for i, item in enumerate(data):
        ic(i, item)
        processed = item / 2
        ic(processed)
        result.append(processed)
    
    ic(result)
    return result

if __name__ == "__main__":
    print("=== 基础调试 ===")
    # debug_example()  # 取消注释来调试
    
    print("\n=== icecream 调试 ===")
    better_debug_example()
