# -*- coding: utf-8 -*-
# 挑战二：配置合并器
import copy

def merge_configs(defaults, user_config, override_mode="replace"):
    """
    合并默认配置和用户配置。
    
    Args:
        defaults: 默认配置字典
        user_config: 用户配置字典
        override_mode: "replace" 或 "extend"
    
    Returns:
        合并后的配置字典（新对象）
    """
    # TODO: 深拷贝默认配置作为基础
    
    # TODO: 根据override_mode选择合并策略
    # - replace: 直接更新
    # - extend: 列表拼接，字典递归合并
    
    pass


# 测试
if __name__ == "__main__":
    defaults = {"db": {"host": "localhost", "port": 3306}, "features": ["auth"], "debug": False}
    user = {"db": {"port": 5432, "name": "mydb"}, "features": ["cache"], "debug": True}
    
    print("Replace:", merge_configs(defaults, user, "replace"))
    print("Extend:", merge_configs(defaults, user, "extend"))
