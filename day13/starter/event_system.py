"""
Day 13 - OOP深入① 类的深层机制
===============================
练习：实现一个 EventEmitter 事件系统

要求：
- 使用描述符(descriptor)管理事件注册
- 支持 on/emit/off 操作
- 理解类属性 vs 实例属性的区别

运行本文件测试你的实现是否正确。
"""


class EventDescriptor:
    """事件描述符 -- 用描述符来管理事件的注册和触发

    TODO: 实现描述符的 __get__ 方法
        - 当从类访问时，返回描述符自身或默认管理器
        - 当从实例访问时，绑定到实例上（懒创建）
    """

    def __init__(self, event_name):
        self.event_name = event_name

    def __set_name__(self, owner, name):
        self.attr_name = name

    # TODO: 实现 __get__(self, instance, owner)
    #       instance is None 时返回描述符自身
    #       否则在 instance.__dict__ 中懒创建 EventEmitter 并返回


class EventEmitter:
    """事件发射器基类

    所有需要事件功能的类都可以继承此类。

    使用示例:
        emitter = EventEmitter()
        emitter.on('click', lambda x: print(f'clicked: {x}'))
        emitter.emit('click', 'button1')
    """

    def __init__(self):
        self._events = {}   # {'event_name': [callback1, callback2, ...]}

    def on(self, event_name, callback=None):
        """注册事件监听器

        支持两种用法：
        1. 作为装饰器:  @emitter.on('click')
        2. 直接调用:   emitter.on('click', my_func)

        Args:
            event_name: 事件名称
            callback: 回调函数（可选，为None时作为装饰器使用）

        TODO: 实现装饰器模式
            - callback 为 None -> 返回装饰器函数
            - callback 不为 None -> 直接注册并返回 callback
        """
        if callback is None:
            # TODO: 返回一个装饰器
            pass
        else:
            # TODO: 将 callback 加入 self._events[event_name]
            pass

    def emit(self, event_name, *args, **kwargs):
        """触发事件

        TODO: 遍历并调用所有注册的回调
            - 事件不存在时静默跳过（或打印警告）
            - 捕获单个回调异常，不影响其余回调
        """
        pass

    def off(self, event_name, callback=None):
        """移除事件监听器

        Args:
            event_name: 事件名称
            callback: 要移除的回调。None 则移除该事件的全部回调

        TODO: 实现移除逻辑
        """
        pass

    def once(self, event_name, callback):
        """注册只触发一次的监听器

        TODO: 实现一次性监听
            - 包装 callback，触发后自动 off
        """
        pass

    def listener_count(self, event_name):
        """返回指定事件的监听器数量"""
        # TODO: 实现计数
        pass


# ==================== 测试 ====================
if __name__ == '__main__':
    print('=' * 50)
    print('Day 13 练习: EventEmitter 事件系统')
    print('=' * 50)

    emitter = EventEmitter()
    results = []

    def on_click(data):
        results.append(f'clicked: {data}')

    emitter.on('click', on_click)
    emitter.emit('click', 'button_A')

    @emitter.on('hover')
    def on_hover(element):
        results.append(f'hovered: {element}')

    emitter.emit('hover', 'nav_bar')

    counter = {'value': 0}

    def on_load():
        counter['value'] += 1

    emitter.once('load', on_load)
    emitter.emit('load')
    emitter.emit('load')  # 第二次不应触发

    assert results == ['clicked: button_A', 'hovered: nav_bar'], f'results: {results}'
    assert counter['value'] == 1, f'once 触发次数: {counter["value"]}'
    assert emitter.listener_count('click') == 1
    assert emitter.listener_count('hover') == 1

    emitter.off('click')
    assert emitter.listener_count('click') == 0

    print('OK -- 所有测试通过!')
