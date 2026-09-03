"""Boss: EventEmitter 事件系统 - 起手代码"""

class EventEmitter:
    """事件发射器基类"""

    def __init__(self):
        # TODO: 初始化事件存储
        pass

    def on(self, event, callback, priority=0):
        # TODO: 注册事件监听
        pass

    def once(self, event, callback, priority=0):
        # TODO: 注册一次性监听
        pass

    def emit(self, event, *args, **kwargs):
        # TODO: 触发事件
        pass

    def off(self, event, callback=None):
        # TODO: 移除监听
        pass

    def listeners(self, event):
        # TODO: 返回事件监听列表
        pass

class Event:
    """事件描述符"""

    def __init__(self, event_name):
        # TODO
        pass

    def __set_name__(self, owner, name):
        # TODO
        pass

    def __get__(self, obj, objtype=None):
        # TODO: 返回可操作的事件对象
        pass

# 测试
if __name__ == '__main__':
    em = EventEmitter()
    em.on('data', lambda x: print(f'received: {x}'))
    em.emit('data', 'hello')

    class Button(EventEmitter):
        click = Event('click')

    btn = Button()
    btn.on('click', lambda: print('clicked'))
    btn.click.emit()
