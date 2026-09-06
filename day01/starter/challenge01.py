# Day 1 挑战一：函数输入、return 与字典增改
# 难度：★☆☆☆☆
#
# 新版 Day 1 不学习 *args / **kwargs。
# 目标：写一个普通函数，接收 name 和 age，返回一份个人信息字典。


def create_person(name, age,city):
    """根据姓名和年龄创建个人信息。

    参数：
        name: 姓名，例如 "Alice"
        age: 年龄，例如 25

    返回：
        {"姓名": name, "年龄": age}
    """
    person = {}

    # 你已经会的字典添加：字典[键] = 值
    person["姓名"] = name
    person["年龄"] = age
    person["城市"] = city

    return person


# ===== 测试 =====
if __name__ == "__main__":
    result1 = create_person("Alice", 25,None)
    print("测试 1：", result1)
    # 期望：{'姓名': 'Alice', '年龄': 25}

    result2 = create_person("小戡", 9,None)
    print("测试 2：", result2)
    # 期望：{'姓名': '小戡', '年龄': 9}

    # 小练习：给 create_person 增加 city 参数，
    # 再写：person["城市"] = city
    result3 = create_person("name", 10,"city")
    print("测试3：", result3)