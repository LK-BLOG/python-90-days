# Day 1 终极挑战：个人信息报告
# 难度：★★★★☆
#
# 这是挑战1～5的组合，但不引入新知识。
# 只用：普通参数、字典、列表、for、print、return。


def build_person_report(name, age, city, hobbies):
    """创建并返回一个人的信息字典。"""
    # TODO：创建空字典
    # TODO：逐个添加“姓名”“年龄”“城市”“爱好”四个键
    # TODO：返回字典
    people_key_word={}
    people_key_word["姓名"] = name
    people_key_word["年龄"] = age
    people_key_word["城市"] = city
    people_key_word["爱好"] = hobbies
    return people_key_word


def show_person_report(person):
    """把个人信息字典逐行打印出来。"""
    # TODO：遍历 person 字典
    # TODO：每次打印一个 key 和 value
    for key, value in person.items():
        print(key, ":",value)


if __name__ == "__main__":
    person = build_person_report("小戡", 9, "北京", ["编程", "游戏"])
    show_person_report(person)
