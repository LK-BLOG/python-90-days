# Day 1 挑战二：简单配置覆盖
# 难度：★★☆☆☆
#
# 不处理嵌套字典；不处理递归；只练习“字典增加/覆盖键值”。


def merge_config(default, override):
    """合并两个普通配置字典，override 覆盖 default。

    示例：
        default = {"name": "小戡", "age": 9}
        override = {"age": 10, "city": "北京"}

        merge_config(default, override)
        # {"name": "小戡", "age": 10, "city": "北京"}

    要求：
        1. 不修改 default；
        2. 不修改 override；
        3. 返回一个新的字典。
    """
    # 第一步：复制 default，例如 result = default.copy()
    # 第二步：遍历 override 的每个 key
    # 第三步：用 result[key] = override[key] 新增或覆盖
    pass


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
