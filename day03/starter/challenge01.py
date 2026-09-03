# Day 3 挑战一：作用域追踪 (★☆☆☆☆)
# 难度: ★☆☆☆☆
# 要求: 预测变量输出，理解 LEGB 作用域规则。


# ===== 任务: 预测每段代码的输出，然后运行验证 =====

# 示例1: 全局 vs 局部
x = 10

def func_a():
    x = 20
    print(f"func_a 内: x = {x}")   # 预测: ?

func_a()
print(f"func_a 外: x = {x}")       # 预测: ?

# 示例2: global 关键字
y = 100

def func_b():
    global y
    y = 200
    print(f"func_b 内: y = {y}")   # 预测: ?

func_b()
print(f"func_b 外: y = {y}")       # 预测: ?

# 示例3: 闭包变量追踪
def outer():
    count = 0
    
    def inner():
        nonlocal count
        count += 1
        return count
    
    return inner

counter = outer()
print(f"\n第一次调用: {counter()}")  # 预测: ?
print(f"第二次调用: {counter()}")    # 预测: ?
print(f"第三次调用: {counter()}")    # 预测: ?

# 示例4: LEGB 查找顺序
x = "global"

def leg_demo():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(f"inner 查找 x: {x}")
    
    inner()
    print(f"leg_demo 查找 x: {x}")

leg_demo()
print(f"全局查找 x: {x}")

# ===== 任务: 写出作用域链 =====
def scope_chain_demo():
    """分析以下代码的作用域链，写出每个 print 的输出。
    
    请在 TODO 处填写你的预测答案，然后运行代码验证。
    """
    a = 1
    
    def level1():
        b = 2
        
        def level2():
            c = 3
            # TODO: 这里能访问 a, b, c 吗？为什么？
            pass
        
        # TODO: 这里能访问 c 吗？为什么？
        pass
    
    # TODO: 这里能访问 b, c 吗？为什么？
    pass


# ===== 测试 =====
if __name__ == "__main__":
    print("=== 作用域追踪测试 ===")
    scope_chain_demo()
    print("\n请确认你的预测是否正确！")
