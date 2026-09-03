# -*- coding: utf-8 -*-
import json
import csv
from io import StringIO

class LoadError(Exception):
    """数据加载错误"""
    pass

def load_data(source, format=None):
    """从多种来源加载数据"""
    # TODO: 检测或使用指定格式
    # TODO: 支持JSON/CSV/字符串/字典
    # TODO: 完整错误处理
    pass
