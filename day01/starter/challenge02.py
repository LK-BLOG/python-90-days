# Day 1 挑战二：简单配置覆盖
# 难度：★★☆☆☆
#
# 只处理普通字典：不嵌套、不递归、不使用 deep_merge。


def merge_config(default, override):
    """把 override 合并进 default，后面的值覆盖前面的值。

    例子：
        default = {"name": "小戡", "age": 9}
        override = {"age": 10, "city": "北京"}

        返回：
        {"name": "小戡", "age": 10, "city": "北京"}

    注意：不要修改 default 本身。
    """
    # copy()：先复制一份，避免改坏 default。
    result = default.copy()

    # for key in override：key 会依次是 "age"、"city"。
    for key in override:
        # 如果 key 已存在，就覆盖；不存在，就新增。
        result[key] = override[key]

    return result


# ===== 测试 =====
if __name__ == "__main__":
    default = {"name": "小戡", "age": 9}
    override = {"age": 10, "city": "北京"}

    result = merge_config(default, override)

    print("合并结果：", result)
    print("原始 default：", default)
    print("原始 override：", override)

    # 期望：
    # 合并结果： {'name': '小戡', 'age': 10, 'city': '北京'}
    # 原始 default： {'name': '小戡', 'age': 9}
    # 原始 override： {'age': 10, 'city': '北京'}

    # 小练习：把 override 改成 {"name": "新名字"}，看看发生什么。
