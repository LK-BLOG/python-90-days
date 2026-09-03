# -*- coding: utf-8 -*-
# 挑战三：函数调度器

class Dispatcher:
    """函数调度器"""

    def __init__(self):
        # TODO: 初始化映射字典
        pass

    def register(self, action, func):
        """注册一个操作"""
        # TODO
        pass

    def dispatch(self, action, **params):
        """调度执行操作"""
        # TODO: 查找并调用函数
        # TODO: 未找到返回错误信息
        pass

    def list_actions(self):
        """列出所有已注册的action"""
        # TODO
        pass


if __name__ == "__main__":
    d = Dispatcher()
    d.register("add", lambda a, b: a + b)
    d.register("multiply", lambda a, b: a * b)
    print(d.dispatch("add", a=3, b=5))
    print(d.dispatch("multiply", a=3, b=5))
    print(d.dispatch("unknown"))
    print(d.list_actions())
