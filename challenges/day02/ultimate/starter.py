# -*- coding: utf-8 -*-
# Boss: 数据管道处理系统

def pipeline(data, *transforms):
    """依次应用多个转换函数"""
    # TODO
    pass

def compose(*funcs):
    """组合多个函数为一个"""
    # TODO
    pass

def pipe(data):
    """链式调用版本"""
    class PipeChain:
        def __init__(self, data):
            # TODO
            pass
        def through(self, func):
            # TODO
            pass
        def result(self):
            # TODO
            pass
    return PipeChain(data)

# 转换函数
def remove_none(data):
    # TODO
    pass

def flatten(data):
    # TODO
    pass

def unique(data):
    # TODO
    pass

def sort_by(key=None, reverse=False):
    # TODO
    pass

def group_by(key):
    # TODO
    pass
