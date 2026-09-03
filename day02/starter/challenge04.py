# Day 2 挑战四：回调系统 (★★★★☆)
# 难度: ★★★★☆
# 要求: 实现事件回调系统。


class EventEmitter:
    """事件发射器 —— 实现发布-订阅模式。
    
    功能说明:
        支持注册事件监听器、触发事件、移除监听器、
        一次性监听器、带优先级的监听器。
    
    用法:
        >>> emitter = EventEmitter()
        >>> emitter.on("data", lambda d: print(f"收到: {d}"))
        >>> emitter.emit("data", "hello")
        收到: hello
    
    支持的特性:
        - on(event, callback): 注册普通监听器
        - once(event, callback): 注册一次性监听器
        - off(event, callback): 移除监听器
        - emit(event, *args, **kwargs): 触发事件
        - on_priority(event, callback, priority): 带优先级的监听器
    """
    
    def __init__(self):
        """初始化事件发射器。"""
        # TODO: 初始化事件存储
        # 提示: self._listeners = {}  # {event_name: [(callback, is_once, priority)]}
        pass
    
    def on(self, event, callback):
        """注册事件监听器。
        
        Args:
            event: 事件名称
            callback: 回调函数
        
        Returns:
            self: 返回自身，支持链式调用
        """
        # TODO: 将 callback 添加到 self._listeners[event] 中
        pass
    
    def once(self, event, callback):
        """注册一次性事件监听器（触发一次后自动移除）。
        
        Args:
            event: 事件名称
            callback: 回调函数
        
        Returns:
            self: 返回自身，支持链式调用
        """
        # TODO: 添加 callback 并标记为 once
        pass
    
    def off(self, event, callback=None):
        """移除事件监听器。
        
        Args:
            event: 事件名称
            callback: 要移除的回调函数；为 None 时移除该事件的所有监听器
        
        Returns:
            self: 返回自身，支持链式调用
        """
        # TODO: 从 self._listeners[event] 中移除指定 callback
        pass
    
    def emit(self, event, *args, **kwargs):
        """触发事件，调用所有注册的监听器。
        
        功能说明:
            按注册顺序（或优先级）调用所有监听器。
            一次性监听器在调用后自动移除。
        
        Args:
            event: 事件名称
            *args: 传递给监听器的位置参数
            **kwargs: 传递给监听器的关键字参数
        
        Returns:
            bool: 是否有监听器被触发
        """
        # TODO: 遍历 self._listeners[event]
        # TODO: 按优先级排序后依次调用
        # TODO: 移除 once 标记的已触发监听器
        pass
    
    def listener_count(self, event):
        """获取指定事件的监听器数量。
        
        Args:
            event: 事件名称
        
        Returns:
            int: 监听器数量
        """
        # TODO: 返回监听器数量
        pass


# ===== 测试 =====
if __name__ == "__main__":
    emitter = EventEmitter()
    
    # 基础监听
    emitter.on("message", lambda msg: print(f"收到消息: {msg}"))
    emitter.emit("message", "Hello World")
    
    # 一次性监听
    def on_connect():
        print("连接建立！（只会打印一次）")
    emitter.once("connect", on_connect)
    emitter.emit("connect")
    emitter.emit("connect")  # 第二次不会触发
    
    print(f"\nmessage 监听器数量: {emitter.listener_count('message')}")
